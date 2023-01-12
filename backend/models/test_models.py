#!/usr/bin/python3
import engine
from models.search import SearchOrm
from models.user import UserOrm
from models.vault import VaultOrm
from pprint import pprint


classes = {
    "User": UserOrm,
    "Vault": VaultOrm,
    "Search": SearchOrm,
}

for cls in classes.values():
    if cls == UserOrm:
        kwargs = {
            "username": "Kizaru",
            "password": "89131231234342"
        }
        my_model = UserOrm(**kwargs)
        user_id = my_model.user_id
    elif cls == VaultOrm:
        kwargs = {
            "name": "Akainu",
            "count": "12",
            "user_id": 1
        }
        my_model = VaultOrm(**kwargs)
        my_model.save()
        # vault_id = my_model.vault_id
    elif cls == SearchOrm:
        kwargs = {
            "word": "Kaizoku",
            "vault_id": 1
        }
        my_model = SearchOrm(**kwargs)
        search_id = my_model.search_id
    else:
        continue
    my_model.save()
    print('\n<---->')
    # my_model = cls[1].from_orm(my_model)
    pprint(my_model)

    print('\n<---->')
    my_model_json = my_model.to_dict()
    pprint(my_model_json)

    print('\n<---->')
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(key,
                                       type(my_model_json[key]),
                                       my_model_json[key]))

    print('\n<---->')
    print("All objects: {}".format(engine.storage.count()))
    print("{} objects: {}".format(cls.__name__, engine.storage.count(cls)))

    print('\n<---->')
    first_cls_id = [obj for obj in engine.storage.all(cls).values()][0].id
    print("First {}: {}".format(str(cls.__name__).lower(),
                                str(engine.storage.get(cls, first_cls_id))))

    # print('\n<---->')
    # my_model.delete()
    # print(storage.all().get(
    #     f"{my_model.__class__.__name__}.{my_model.id}"))
