# import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

# require jwt for api access
from flask_jwt_extended import jwt_required, get_jwt

# SQLAlchemyError is base exception for sqlalchemy errors
from sqlalchemy.exc import SQLAlchemyError

from models import ItemModel
from db import db

# from db import items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()
        
        return item


@blp.route("/item")
class ItemList(MethodView):
    # http://127.0.0.1:5000/store
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    # jwt_required() - require jwt token for api access
    @jwt_required(fresh=True)   # fresh=True - require fresh token for deleteing or creating item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting item into table.")
        # Commented due to marshmallow implementation

        # if (
        #     "price" not in item_data
        #     or "store_id" not in item_data
        #     or "name" not in item_data
        # ):
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'price', 'store_id', 'name' are included in JSON payload ",
        #     )

        # # Check if item already exists in the items
        # for item in items.values():
        #     if (
        #         item["name"] == item_data["name"]
        #         and item["store_id"] == item_data["store_id"]
        #     ):
        #         abort(400, description="Item already exists.")

        # item_id = uuid.uuid4().hex
        # item = {**item_data, "id": item_id}
        # items[item_id] = item
        return item, 201
