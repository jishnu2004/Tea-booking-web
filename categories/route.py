from flask import Flask,request,jsonify, render_template
import json
from tea import tea
#db import
from tea import db
# models import 
from .models import * 

@tea.route("/category/create", methods=["POST"])
def categoryCreate():
    try:
        request_json = request.get_json()
        Category(name = request_json["name"]).save()
        responce={}    
        responce['status'] = True
        responce['status_code'] = 200
        responce['data'] = []
        responce['description'] = 'creation success'
        return jsonify(responce)
    except Exception as err:
        responce={}    
        responce['status'] = False
        responce['status_code'] = 304
        responce['data'] = []
        responce['description'] = 'A Batch with this name exists'+str(err)
        return jsonify(responce)
    
@tea.route("/category/get", methods=["POST"])
def show_list():
    try:
        request_json = request.get_json()
        category_list = json.loads(Category.objects().to_json())
        responce={}    
        responce['status'] = True
        responce['status_code'] = 200
        responce['data'] = category_list
        responce['description'] = 'creation success'
        return jsonify(responce)
    except Exception as err:
        responce={}    
        responce['status'] = False
        responce['status_code'] = 304
        responce['data'] = []
        responce['description'] = 'A Batch with this name exists'+str(err)
        return jsonify(responce)
    


# @tea.route("/product/create", methods=["POST"])
# def productCreate():
#     try:
#         request_json = request.get_json()
#         Product(name = request_json["name"],category = request_json["category"]).save()
#         # Product(category = request_json["category"]).save()
#         responce={}    
#         responce['status'] = True
#         responce['status_code'] = 200
#         responce['data'] = []
#         responce['description'] = 'creation success'
#         return jsonify(responce)
#     except Exception as err:
#         responce={}    
#         responce['status'] = False
#         responce['status_code'] = 304
#         responce['data'] = []
#         responce['description'] = 'A Batch with this name exists'+str(err)
#         return jsonify(responce)


# print all products
@tea.route("/product/get", methods=["POST"])
def product_list():
    try:
        request_json = request.get_json()
        product_list = json.loads(Product.objects().to_json())
        responce={}    
        responce['status'] = True
        responce['status_code'] = 200
        responce['data'] = product_list
        responce['description'] = 'creation success'
        return jsonify(responce)
    except Exception as err:
        responce={}    
        responce['status'] = False
        responce['status_code'] = 304
        responce['data'] = []
        responce['description'] = 'A Batch with this name exists'+str(err)
        return jsonify(responce)



@tea.route("/product/category_create", methods=["POST"])
def product_create():
    try:
        request_json = request.get_json()
        category_name = request_json.get("category_name")
        product_name = request_json.get("product_name")
        myurl = request_json.get("myurl")

        # Retrieve the category from the database
        category = Category.objects(name=category_name).first()

        if not category:
            return jsonify({
                "status": False,
                "status_code": 404,
                "description": f"Category '{category_name}' not found"
            }), 404

        # Create a new product instance
        product = Product(name=product_name, imgurl=myurl, category=category)
        product.save()

        return jsonify({
            "status": True,
            "status_code": 200,
            "description": "Product added successfully"
        }), 200
    except Exception as err:
        return jsonify({
            "status": False,
            "status_code": 500,
            "description": f"Error adding product: {err}"
        }), 500




# @tea.route("/products/<category_name>", methods=["POST"])
# def products_in_category(category_name):
#     try:
#         # Retrieve the category from the database
#         category = Category.objects(name=category_name).first()

#         if not category:
#             return jsonify({
#                 "status": False,
#                 "status_code": 404,
#                 "description": f"Category '{category_name}' not found"
#             }), 404

#         # Retrieve products belonging to the category
#         products = Product.objects(category=category)

#         product_list = []
#         for product in products:
#             product_data = {
#                 "name": product.name,
#                 "category": product.category.name
#             }
#             product_list.append(product_data)
#             # responce['data'] = product_list

#         return jsonify({
#             "status": True,
#             "status_code": 200,
#             "data": product_list,
#             "description": f"Products in category '{category_name}'"
#         }), 200
#     except Exception as err:
#         return jsonify({
#             "status": False,
#             "status_code": 500,
#             "description": f"Error fetching products: {err}"
#         }), 500
    
@tea.route("/products", methods=["POST"])
def products_in_category_post():
    try:
        # Extract category name from request JSON
        request_json = request.get_json()
        category_name = request_json.get("category_name")

        if not category_name:
            return jsonify({
                "status": False,
                "status_code": 400,
                "description": "Category name is required in the request JSON"
            }), 400

        # Retrieve the category from the database
        category = Category.objects(name=category_name).first()

        if not category:
            return jsonify({
                "status": False,
                "status_code": 404,
                "description": f"Category '{category_name}' not found"
            }), 404

        # Retrieve products belonging to the category
        products = Product.objects(category=category)

        product_list = []
        for product in products:
            product_data = {
                "name": product.name,
                "category": product.category.name
            }
            product_list.append(product_data)

        return jsonify({
            "status": True,
            "status_code": 200,
            "data": product_list,
            "description": f"Products in category '{category_name}'"
        }), 200
    except Exception as err:
        return jsonify({
            "status": False,
            "status_code": 500,
            "description": f"Error fetching products: {err}"
        }), 500
    

# @tea.route("/product/update/<product_id>", methods=["PUT"])
# def update_product(product_id):
#     try:
#         # Retrieve the product from the database
#         product = Product.objects(id=product_id).first()

#         if not product:
#             return jsonify({
#                 "status": False,
#                 "status_code": 404,
#                 "description": f"Product with ID '{product_id}' not found"
#             }), 404

#         # Update product fields based on request data
#         request_json = request.get_json()
#         product.name = request_json.get("name", product.name)
#         # product.category = request_json.get("category", product.category)
#         # product.price = request_json.get("price", product.price)
#         product.save()

#         return jsonify({
#             "status": True,
#             "status_code": 200,
#             "description": f"Product with ID '{product_id}' updated successfully"
#         }), 200
#     except Exception as err:
#         return jsonify({
#             "status": False,
#             "status_code": 500,
#             "description": f"Error updating product: {err}"
#         }), 500
    

@tea.route("/product/update", methods=["POST"])
def update_product():
    try:
        # Extract product name from request JSON
        request_json = request.get_json()
        product_name = request_json.get("product_name")

        if not product_name:
            return jsonify({
                "status": False,
                "status_code": 400,
                "description": "Product name is required in the request JSON"
            }), 400

        # Retrieve the product from the database based on the product name
        product = Product.objects(name=product_name).first()

        if not product:
            return jsonify({
                "status": False,
                "status_code": 404,
                "description": f"Product '{product_name}' not found"
            }), 404

        # Update product fields based on request data
        product.name = request_json.get("name", product.name)
        # product.category = request_json.get("category", product.category)
        # product.price = request_json.get("price", product.price)
        product.save()

        return jsonify({
            "status": True,
            "status_code": 200,
            "description": f"Product '{product_name}' updated successfully"
        }), 200
    except Exception as err:
        return jsonify({
            "status": False,
            "status_code": 500,
            "description": f"Error updating product: {err}"
        }), 500 



    
# @tea.route("/product/delete/<product_id>", methods=["DELETE"])
# def delete_product(product_id):
#     try:
#         # Retrieve the product from the database
#         product = Product.objects(id=product_id).first()

#         if not product:
#             return jsonify({
#                 "status": False,
#                 "status_code": 404,
#                 "description": f"Product with ID '{product_id}' not found"
#             }), 404

#         # Delete the product
#         product.delete()

#         return jsonify({
#             "status": True,
#             "status_code": 200,
#             "description": f"Product with ID '{product_id}' deleted successfully"
#         }), 200
#     except Exception as err:
#         return jsonify({
#             "status": False,
#             "status_code": 500,
#             "description": f"Error deleting product: {err}"
#         }), 500



@tea.route("/product/delete", methods=["POST"])
def delete_product_by_name():
    try:
        # Extract product name from request JSON
        request_json = request.get_json()
        product_name = request_json.get("product_name")

        if not product_name:
            return jsonify({
                "status": False,
                "status_code": 400,
                "description": "Product name is required in the request JSON"
            }), 400

        # Retrieve the product from the database based on the product name
        product = Product.objects(name=product_name).first()

        if not product:
            return jsonify({
                "status": False,
                "status_code": 404,
                "description": f"Product '{product_name}' not found"
            }), 404

        # Delete the product
        product.delete()

        return jsonify({
            "status": True,
            "status_code": 200,
            "description": f"Product '{product_name}' deleted successfully"
        }), 200
    except Exception as err:
        return jsonify({
            "status": False,
            "status_code": 500,
            "description": f"Error deleting product: {err}"
        }), 500




# @tea.route("/product/update_category/<product_id>", methods=["PUT"])
# def update_product_category(product_id):
#     try:
#         # Retrieve the product from the database
#         product = Product.objects(id=product_id).first()

#         if not product:
#             return jsonify({
#                 "status": False,
#                 "status_code": 404,
#                 "description": f"Product with ID '{product_id}' not found"
#             }), 404

#         # Retrieve the new category from the request
#         request_json = request.get_json()
#         new_category_name = request_json.get("category_name")

#         # Check if the category already exists
#         new_category = Category.objects(name=new_category_name).first()

#         # If category doesn't exist, create a new one
#         if not new_category:
#             new_category = Category(name=new_category_name)
#             new_category.save()

#         # Update the product's category
#         product.category = new_category
#         product.save()

#         return jsonify({
#             "status": True,
#             "status_code": 200,
#             "description": f"Product with ID '{product_id}' category updated successfully"
#         }), 200
#     except Exception as err:
#         return jsonify({
#             "status": False,
#             "status_code": 500,
#             "description": f"Error updating product category: {err}"
#         }), 500



@tea.route("/product/update_category", methods=["POST"])
def update_product_category_by_name():
    try:
        # Extract product name and new category name from request JSON
        request_json = request.get_json()
        product_name = request_json.get("product_name")
        new_category_name = request_json.get("category_name")

        if not product_name or not new_category_name:
            return jsonify({
                "status": False,
                "status_code": 400,
                "description": "Product name and new category name are required in the request JSON"
            }), 400

        # Retrieve the product from the database based on the product name
        product = Product.objects(name=product_name).first()

        if not product:
            return jsonify({
                "status": False,
                "status_code": 404,
                "description": f"Product '{product_name}' not found"
            }), 404

        # Check if the category already exists
        new_category = Category.objects(name=new_category_name).first()

        # If category doesn't exist, create a new one
        if not new_category:
            new_category = Category(name=new_category_name)
            new_category.save()

        # Update the product's category
        product.category = new_category
        product.save()

        return jsonify({
            "status": True,
            "status_code": 200,
            "description": f"Product '{product_name}' category updated successfully"
        }), 200
    except Exception as err:
        return jsonify({
            "status": False,
            "status_code": 500,
            "description": f"Error updating product category: {err}"
        }), 500


@tea.route("/category/delete", methods=["POST"])
def delete_category_by_name():
    try:
        # Extract product name from request JSON
        request_json = request.get_json()
        category_name = request_json.get("category_name")

        if not category_name:
            return jsonify({
                "status": False,
                "status_code": 400,
                "description": "category name is required in the request JSON"
            }), 400

        # Retrieve the product from the database based on the product name
        category = Category.objects(name=category_name).first()

        if not category:
            return jsonify({
                "status": False,
                "status_code": 404,
                "description": f"Category  '{category_name}' not found"
            }), 404

        # Delete the product
        category.delete()

        return jsonify({
            "status": True,
            "status_code": 200,
            "description": f"Product '{category_name}' deleted successfully"
        }), 200
    except Exception as err:
        return jsonify({
            "status": False,
            "status_code": 500,
            "description": f"Error deleting product: {err}"
        }), 500
    

    # New route for new project
#org creation
@tea.route('/organization/creation', methods=['POST'])
def organizations_add():
    try:
        request_data = request.get_json()
        org_name= request_data['org_name']
        description= request_data['description']
        created_person= request_data['created_person']
        source= request_data['source']
        type= request_data['type']
        org_name_lower = org_name.lower()
        if Organizations.objects(org_name__iexact=org_name_lower):
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "Organization name already exists"
            return jsonify(response)
        if org_name and description and created_person:
            organizations = Organizations(org_name=org_name, description=description,created_person=created_person,source=source,type=type).save()
            organizations.org_id = str(organizations.id)
            organizations.save()
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = [{"org_id": str(organizations.id)}]
            response['description'] = 'org creation successful'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
    
#org reading
@tea.route('/organizations/list', methods=['GET'])
def list_organizations():
    try:
        org = Organizations.objects().to_json()
        df = json.loads(org)
        response={}    
        response['status'] = True
        response['status_code'] = 200
        response['data'] =df
        response['description'] = 'organisations list'
        return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)



#get single org
@tea.route('/organization/get', methods=['POST'])
def organization_get():
    try:
        request_data = request.json
        org_id = request_data['org_id']
        data=Organizations.objects(org_id=org_id)
        if data:
            df=data.to_json()
            df = json.loads(df)
            response = {}
            response['status'] = True
            response['status_code'] = 200
            response['data'] =df
            response['description'] = 'Organization Data Fetched succesfully'
            return response
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no organisation found'
            return response
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)        


#update org
@tea.route('/organization/edit', methods=['POST'])
def org_edit():
    try:
        request_data = request.get_json()
        org_id= request_data['org_id']
        org_name= request_data['org_name']
        description= request_data['description']
        status= request_data['status']
        source= request_data['source']
        type= request_data['type']
        if org_name and description and status:
            Organizations.objects(org_id=org_id).update(set__org_name=org_name,set__description=description,set__status=status,set__source=source,set__type=type)
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = []
            response['description'] = 'successfully edited'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)    
        
       

#org delete
@tea.route('/organization/delete', methods=['POST'])
def delete_organization():
    try:
        request_data = request.get_json()
        org_id= request_data['org_id']
        organizations = Organizations.objects(org_id=org_id).first()

        if organizations:
            organizations.delete()
            response={}
            response["status"]=True
            response['description']="Organization data Deleted successfully!"
            response["status_code"]=200
            response["data"]=[]
            return jsonify(response)
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no organisation found'
            return response

    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)






# location creation
@tea.route('/Location/creation', methods=['POST'])
def location_add():
    try:
        request_data = request.get_json()

        org_name = request_data['org_name']
        org = Organizations.objects(org_name=org_name).first()
        if not org:
            return jsonify({
                "status": False,
                "status_code": 404,
                "description": f"Category '{org_name}' not found"
            }), 404

        locationName= request_data['locationName']
        country=request_data['country']
        state=request_data['state']
        city=request_data['city']
        zipCode=request_data['zipCode']
        latitude=request_data['latitude']
        longitude=request_data['longitude']
        locationName_lower = locationName.lower()
        if Location.objects(locationName__iexact=locationName_lower):
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "location name already exists"
            return jsonify(response)
        if locationName and country and state and city and zipCode and latitude and longitude:
            location = Location(locationName=locationName, country=country,state=state,city=city,zipCode=zipCode,latitude=latitude,longitude=longitude,org=org).save()
            location.id = str(location.id)
            location.save()
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = [{'id': str(location.id)}]
            response['description'] = 'location creation successful'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
    

#get a single location details
@tea.route('/Location/get', methods=['POST'])
def location_get():
    try:
        request_data = request.json
        id = request_data['id']
        data=Location.objects(id=id)
        if data:
            df=data.to_json()
            df = json.loads(df)
            response = {}
            response['status'] = True
            response['status_code'] = 200
            response['data'] =df
            response['description'] = 'Location Data Fetched succesfully'
            return response
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no location found'
            return response
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)

#LOCATION DETAILS READING BASED ON ORGANIZATION ID
@tea.route('/Location/get_all_by_org', methods=['POST'])
def get_all_loaction_by_org():
    try:
        request_data = request.json
        org = request_data['org']
        loc= Location.objects(org=org)

        if loc:
            # Convert the queryset to JSON
            loc_json = loc.to_json()

            response = {
                'status': True,
                'status_code': 200,
                'data': json.loads(loc_json),
                'description': 'location details fetched successfully'
            }
            return jsonify(response)
        else:
            response = {
                'status': False,
                'status_code': 404,
                'data': [],
                'description': 'No location details found for the provided PrizeList'
            }
            return jsonify(response)
    except Exception as e:
        response = {
            'status': False,
            'status_code': 500,
            'data': [],
            'description': str(e)
        }
        return jsonify(response)

#update location
@tea.route('/Location/edit', methods=['POST'])
def location_edit():
    try:
        request_data = request.get_json()
        id=request_data["id"]
        locationName= request_data['locationName']
        country=request_data['country']
        state=request_data['state']
        city=request_data['city']
        zipCode=request_data['zipCode']
        latitude=request_data['latitude']
        longitude=request_data['longitude']
        if locationName and country and state and city and zipCode and latitude and longitude:
            Location.objects(id=id).update(set__locationName=locationName,set__country=country,set__state=state,set__city=city,set__zipCode=zipCode,set__latitude=latitude,set__longitude=longitude)
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = []
            response['description'] = 'successfully edited'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)   



#delete location
@tea.route('/Location/delete', methods=['POST'])
def delete_location():
    try:
        request_data = request.get_json()
        id= request_data['id']
        location = Location.objects(id=id).first()

        if location:
            location.delete()
            response={}
            response["status"]=True
            response['description']="Location data Deleted successfully!"
            response["status_code"]=200
            response["data"]=[]
            return jsonify(response)
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no location found'
            return response

    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)

    


# CustomerGroup creation
@tea.route('/CustomerGroup/creation', methods=['POST'])
def customer_group_add():
    try:
        request_data = request.get_json()

        locationName = request_data['locationName']
        location = Location.objects(locationName=locationName).first()
        if not location:
            return jsonify({
                "status": False,
                "status_code": 404,
                "description": f"Category '{locationName}' not found"
            }), 404
        customer_group_name= request_data['customer_group_name']
        
        customer_group_name_lower = customer_group_name.lower()
        if CustomerGroup.objects(customer_group_name__iexact=customer_group_name_lower):
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "customer group name already exists"
            return jsonify(response)
        if customer_group_name :
            customer_group = CustomerGroup(customer_group_name=customer_group_name,location=location).save()
            customer_group.id = str(customer_group.id)
            customer_group.save()
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = [{'id': str(customer_group.id)}]
            response['description'] = 'customer group creation successful'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
    
#get single customergroup
@tea.route('/CustomerGroup/get', methods=['POST'])
def CustomerGroup_get():
    try:
        request_data = request.json
        id = request_data['id']
        data=CustomerGroup.objects(id=id)
        if data:
            df=data.to_json()
            df = json.loads(df)
            response = {}
            response['status'] = True
            response['status_code'] = 200
            response['data'] =df
            response['description'] = 'Customer Group Data Fetched succesfully'
            return response
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no Customer Group found'
            return response
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)


#update customerGroup
@tea.route('/CustomerGroup/edit', methods=['POST'])
def CustomerGroup_edit():
    try:
        request_data = request.get_json()
        id=request_data["id"]
        customer_group_name= request_data['customer_group_name']
        
        if customer_group_name:
            CustomerGroup.objects(id=id).update(set__customer_group_name=customer_group_name)
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = []
            response['description'] = 'successfully edited'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)



#delete CustomerGroup
@tea.route('/CustomerGroup/delete', methods=['POST'])
def CustomerGroup_delete():
    try:
        request_data = request.get_json()
        id= request_data['id']
        customergroup = CustomerGroup.objects(id=id).first()

        if customergroup:
            customergroup.delete()
            response={}
            response["status"]=True
            response['description']="customergroup data Deleted successfully!"
            response["status_code"]=200
            response["data"]=[]
            return jsonify(response)
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no customergroup found'
            return response

    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)



# Customer creation
@tea.route('/Customer/creation', methods=['POST'])
def customer_add():
    try:
        request_data = request.get_json()
        customer_group_name = request_data['customer_group_name']
        customer_group = CustomerGroup.objects(customer_group_name=customer_group_name).first()
        if not customer_group:
            return jsonify({
                "status": False,
                "status_code": 404,
                "description": f"Category '{customer_group_name}' not found"
            }), 404

        customer_name= request_data['customer_name']
        customer_email=request_data['customer_email']
        customer_phone=request_data['customer_phone']
        
        customer_name_lower = customer_name.lower()
        if Customers.objects(customer_name__iexact=customer_name_lower):
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "customer name already exists"
            return jsonify(response)
        if customer_name and customer_phone and customer_email:
            customer = Customers(customer_name=customer_name ,customer_email=customer_email,customer_phone=customer_phone,customer_group=customer_group).save()
            customer.id = str(customer.id)
            customer.save()
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = [{'id': str(customer.id)}]
            response['description'] = 'customer creation successful'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
    

#get single customer
@tea.route('/Customer/get', methods=['POST'])
def Customer_get():
    try:
        request_data = request.json
        id = request_data['id']
        data=Customers.objects(id=id)
        if data:
            df=data.to_json()
            df = json.loads(df)
            response = {}
            response['status'] = True
            response['status_code'] = 200
            response['data'] =df
            response['description'] = 'Customer Data Fetched succesfully'
            return response
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no Customer found'
            return response
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)


#update customer data
@tea.route('/Customer/edit', methods=['POST'])
def Customer_edit():
    try:
        request_data = request.get_json()
        id=request_data["id"]

        customer_name= request_data['customer_name']
        customer_email=request_data['customer_email']
        customer_phone=request_data['customer_phone']
        
        if customer_name and customer_phone and customer_email:
            Customers.objects(id=id).update(set__customer_name=customer_name,set__customer_email=customer_email,set__customer_phone=customer_phone)
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = []
            response['description'] = 'successfully edited'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)



#delete CustomerGroup
@tea.route('/Customer/delete', methods=['POST'])
def Customer_delete():
    try:
        request_data = request.get_json()
        id= request_data['id']
        customer = Customers.objects(id=id).first()

        if customer:
            customer.delete()
            response={}
            response["status"]=True
            response['description']="customer data Deleted successfully!"
            response["status_code"]=200
            response["data"]=[]
            return jsonify(response)
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no customer found'
            return response

    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
    



# latest api
#crud api for Products
# Create Product
@tea.route('/products/create', methods=['POST'])
def products_create():
    try:
        request_data = request.json
        org_id = request_data['org_id']
        product_name = request_data['product_name']
        product_description = request_data['product_description']

        prodt=Products(product_name=product_name,product_description=product_description,str_org_id=org_id).save()
        prodt.product_id=str(prodt.id)
        prodt.save()
        response={}
        response['status'] = True
        response['status_code'] = 200
        response['data'] = {"product_id":str(prodt.id)}
        response['description'] = 'product created'
        return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)

#PRODUCT DETAILS READING BASED ON ORGANIZATION ID
@tea.route('/products/get_all_by_org', methods=['POST'])
def get_all_products_by_org():
    try:
        request_data = request.json
        org_id = request_data['org_id']
        prodlist= Products.objects(org_id=org_id)

        if prodlist:
            # Convert the queryset to JSON
            prodt_json = prodlist.to_json()

            response = {
                'status': True,
                'status_code': 200,
                'data': json.loads(prodt_json),
                'description': 'Products details fetched successfully'
            }
            return jsonify(response)
        else:
            response = {
                'status': False,
                'status_code': 404,
                'data': [],
                'description': 'No product details found for the provided PrizeList'
            }
            return jsonify(response)
    except Exception as e:
        response = {
            'status': False,
            'status_code': 500,
            'data': [],
            'description': str(e)
        }
        return jsonify(response)

#update product
@tea.route('/products/edit', methods=['POST'])
def products_edit():
    try:
        request_data = request.get_json()
        product_id=request_data["product_id"]

        #org_id = request_data['org_id']
        product_name = request_data['product_name']
        product_description = request_data['product_description']
        
        if product_name and product_description :
            Products.objects(product_id=product_id).update(set__product_name=product_name,set__product_description=product_description)
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = []
            response['description'] = 'product successfully edited'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
    
# read single product
@tea.route('/products/get', methods=['POST'])
def products_get():
    try:
        request_data = request.json
        product_id = request_data['product_id']
        data=Products.objects(product_id=product_id)
        if data:
            df=data.to_json()
            df = json.loads(df)
            response = {}
            response['status'] = True
            response['status_code'] = 200
            response['data'] =df
            response['description'] = 'Product Data Fetched succesfully'
            return response
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no product found'
            return response
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
    
#Delete a product
@tea.route('/products/delete', methods=['POST'])
def products_delete():
    try:
        request_data = request.get_json()
        product_id= request_data['product_id']
        prodt = Products.objects(product_id=product_id).first()

        if prodt:
            prodt.delete()
            response={}
            response["status"]=True
            response['description']="product data Deleted successfully!"
            response["status_code"]=200
            response["data"]=[]
            return jsonify(response)
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no product found'
            return response

    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)   
    

#crud api for PrizeList
# Create Prize list
@tea.route('/PrizeList/create', methods=['POST'])
def prizeList_create():
    try:
        request_data = request.json
        org_id = request_data['org_id']
        product_id = request_data['product_id']
        product_name = request_data['product_name']
        prize = request_data['prize']
        tax = request_data['tax']
        status = request_data['status']
        # str_product_id= request_data['str_product_id']

        przlist=PrizeList(org_id=org_id,product_id=product_id,product_name=product_name,prize=prize,tax=tax,status=status,str_product_id=product_id).save()
        przlist.prizelist_id=str(przlist.id)
        przlist.save()
        response={}
        response['status'] = True
        response['status_code'] = 200
        response['data'] = {"prizelist_id":str(przlist.id)}
        response['description'] = 'prizelist created'
        return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)

#read single prize list
@tea.route('/PrizeList/get', methods=['POST'])
def PrizeList_get():
    try:
        request_data = request.json
        prizelist_id = request_data['prizelist_id']
        data=PrizeList.objects(prizelist_id=prizelist_id)
        if data:
            df=data.to_json()
            df = json.loads(df)
            response = {}
            response['status'] = True
            response['status_code'] = 200
            response['data'] =df
            response['description'] = 'prizelist Data Fetched succesfully'
            return response
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no prizelist found'
            return response
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)

#PRIZELIST DETAILS READING BASED ON PRODUCT ID
@tea.route('/PrizeList/get_all_by_org', methods=['POST'])
def get_all_PrizeList_by_org():
    try:
        request_data = request.json
        product_id = request_data['product_id']
        przlist= PrizeList.objects(product_id=product_id)

        if przlist:
            # Convert the queryset to JSON
            przlst_json = przlist.to_json()

            response = {
                'status': True,
                'status_code': 200,
                'data': json.loads(przlst_json),
                'description': 'Prize list details fetched successfully'
            }
            return jsonify(response)
        else:
            response = {
                'status': False,
                'status_code': 404,
                'data': [],
                'description': 'No prizelist details found for the provided PrizeList'
            }
            return jsonify(response)
    except Exception as e:
        response = {
            'status': False,
            'status_code': 500,
            'data': [],
            'description': str(e)
        }
        return jsonify(response)


#update a pizelist
@tea.route('/PrizeList/edit', methods=['POST'])
def PrizeList_edit():
    try:
        request_data = request.get_json()
        prizelist_id = request_data['prizelist_id']
        prize = request_data['prize']
        tax = request_data['tax']
        status = request_data['status']
        
        if prize and tax and status :
            PrizeList.objects(prizelist_id=prizelist_id).update(set__prize=prize,set__tax=tax,set__status=status)
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = []
            response['description'] = 'prizelist data successfully edited'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
    
    
#deleting prizelist
@tea.route('/PrizeList/delete', methods=['POST'])
def PrizeList_delete():
    try:
        request_data = request.get_json()
        prizelist_id= request_data['prizelist_id']
        przlist = PrizeList.objects(prizelist_id=prizelist_id).first()

        if przlist:
            przlist.delete()
            response={}
            response["status"]=True
            response['description']="prizelist data Deleted successfully!"
            response["status_code"]=200
            response["data"]=[]
            return jsonify(response)
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no prizelist found'
            return response

    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)   

#crud api for Tax
#Creat tax data
@tea.route('/Tax/create', methods=['POST'])
def Tax_create():
    try:
        request_data = request.json
        org_id = request_data['org_id']
        prizelist_id = request_data['prizelist_id']
        tax_amount = request_data['tax_amount']
        status = request_data['status']

        Taxlist=Tax(org_id=org_id,prizelist_id=prizelist_id,tax_amount=tax_amount,status=status).save()
        Taxlist.prizelist_id=str(Taxlist.id)
        Taxlist.save()
        response={}
        response['status'] = True
        response['status_code'] = 200
        response['data'] = {"prizelist_id":str(Taxlist.id)}
        response['description'] = 'prizelist created'
        return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response) 

#READ TAX DETAILS BASED ON PRIZELIST PARENT MODEL
@tea.route('/Tax/get_all_by_prizelist', methods=['POST'])
def Tax_get_all_by_prizelist():
    try:
        request_data = request.json
        prizelist_id = request_data['prizelist_id']

        # Fetch all tax details based on the provided PrizeList ID
        taxes = Tax.objects(prizelist_id=prizelist_id)

        if taxes:
            # Convert the queryset to JSON
            taxes_json = taxes.to_json()

            response = {
                'status': True,
                'status_code': 200,
                'data': json.loads(taxes_json),
                'description': 'Tax details fetched successfully'
            }
            return jsonify(response)
        else:
            response = {
                'status': False,
                'status_code': 404,
                'data': [],
                'description': 'No tax details found for the provided PrizeList'
            }
            return jsonify(response)
    except Exception as e:
        response = {
            'status': False,
            'status_code': 500,
            'data': [],
            'description': str(e)
        }
        return jsonify(response)

#read single tax details
@tea.route('/Tax/get', methods=['POST'])
def Tax_get():
    try:
        request_data = request.json
        tax_id = request_data['tax_id']
        data=Tax.objects(tax_id=tax_id)
        if data:
            df=data.to_json()
            df = json.loads(df)
            response = {}
            response['status'] = True
            response['status_code'] = 200
            response['data'] =df
            response['description'] = 'Tax Data Fetched succesfully'
            return response
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no Tax data found'
            return response
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
    
#update a Tax data
@tea.route('/Tax/edit', methods=['POST'])
def Tax_edit():
    try:
        request_data = request.get_json()
        tax_id = request_data['tax_id']
        tax_amount = request_data['tax_amount']
        
        if tax_amount :
            Tax.objects(tax_id=tax_id).update(set__tax_amount=tax_amount)
            response={}    
            response['status'] = True
            response['status_code'] = 200
            response['data'] = []
            response['description'] = 'Tax data successfully edited'
            return jsonify(response)
        else:
            response={}    
            response['status'] = False
            response['status_code'] = 400
            response['data'] = []
            response['description'] = "please provide all details"
            return jsonify(response)
    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)

#deleting Tax data
@tea.route('/Tax/delete', methods=['POST'])
def Tax_delete():
    try:
        request_data = request.get_json()
        tax_id= request_data['tax_id']
        Taxlist = Tax.objects(tax_id=tax_id).first()

        if Taxlist:
            Taxlist.delete()
            response={}
            response["status"]=True
            response['description']="Tax data Deleted successfully!"
            response["status_code"]=200
            response["data"]=[]
            return jsonify(response)
        else:
            response = {}
            response['status'] = False
            response['status_code'] =404
            response['data'] =[]
            response['description'] = 'no Tax data  found'
            return response

    except Exception as e:
        response={}    
        response['status'] = False
        response['status_code'] = 500
        response['data'] = []
        response['description'] = str(e)
        return jsonify(response)
