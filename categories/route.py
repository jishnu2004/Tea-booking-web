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