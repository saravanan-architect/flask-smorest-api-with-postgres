# SQLAlchemyError is base error for sqlalchemy
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel

# from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200


@blp.route("/store")
class StoreList(MethodView):
    # http://127.0.0.1:5000/store
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    # body data
    # {
    #     "name": "My Store 2"
    # }
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        # grab the incoming json string from client
        # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'name' is included in JSON payload ",
        #     )

        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(500, message="A Store with that name already exists.")

        except SQLAlchemyError:
            abort(500, message="An error occured while inserting item into tables.")

        # for store in stores.values():
        #     if store["name"] == store_data["name"]:
        #         abort(400, description="Store already exists.")

        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store
        return store, 201
