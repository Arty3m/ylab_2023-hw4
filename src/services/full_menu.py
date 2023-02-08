import copy
from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Redis, get_db, get_redis
from src.models import Dish, Menu, SubMenu
from src.services import CRUD


@dataclass
class FullMenu:
    cache: Redis
    crud: CRUD

    async def create_all_menu(self) -> dict:
        menu_1: Menu = Menu(**{"title": "Еда", "description": "Основное меню"})
        menu_1.submenus_count = 2
        menu_1.dishes_count = 5
        await self.crud.add_to_db(menu_1)
        submenu_1_1: SubMenu = SubMenu(**{"title": "Холодные закуски", "description": "К пиву"})
        submenu_1_1.owner = menu_1.id
        submenu_1_1.dishes_count = 2
        await self.crud.add_to_db(submenu_1_1)
        dish_1_1: Dish = Dish(
            **{
                "title": "Сельдь Бисмарк",
                "description": "Традиционное немецкое блюдо из маринованной сельди",
                "price": "182.99",
            },
        )
        dish_1_1.owner = submenu_1_1.id
        dish_1_2: Dish = Dish(
            **{
                "title": "Мясная тарелка",
                "description": "Нарезка из креветок, кальмаров, раковых шеек, гребешков, лосося, скумбрии и красной икры",
                "price": "215.36",
            },
        )
        dish_1_2.owner = submenu_1_1.id
        await self.crud.add_to_db(dish_1_1)
        await self.crud.add_to_db(dish_1_2)
        submenu_1_2: SubMenu = SubMenu(**{"title": "Рамен", "description": " Горячий рамен"})
        submenu_1_2.owner = menu_1.id
        submenu_1_2.dishes_count = 3
        await self.crud.add_to_db(submenu_1_2)
        dish_1_2_1: Dish = Dish(
            **{
                "title": "Дайзу рамен",
                "description": "Рамен на курином бульоне с куриными подушками и яйцом",
                "price": "166.87",
            },
        )
        dish_1_2_1.owner = submenu_1_2.id
        dish_1_2_2: Dish = Dish(
            **{
                "title": "Унаги рамен",
                "description": "Рамен на нежном сливочном рыбном бульоне, с добавлением маринованного угря, "
                "грибов муэр, кунжута, и зеленым луком",
                "price": "165.90",
            },
        )
        dish_1_2_2.owner = submenu_1_2.id
        dish_1_2_3: Dish = Dish(
            **{
                "title": "Чиизу Рамен",
                "description": "Рамен на насыщенном сырном бульоне на основе кокосового молока, с дабавлением"
                " куриной грудинки, яично-пшеничной лапши, ростков зелени, листьев вакамэ",
                "price": "182.99",
            },
        )
        dish_1_2_3.owner = submenu_1_2.id
        await self.crud.add_to_db(dish_1_2_1)
        await self.crud.add_to_db(dish_1_2_2)
        await self.crud.add_to_db(dish_1_2_3)
        ####################################
        menu_2: Menu = Menu(**{"title": "Алкоголь", "description": "Алкогольные напитки"})
        menu_2.submenus_count = 2
        menu_2.dishes_count = 6

        await self.crud.add_to_db(menu_2)
        submenu_2_1 = SubMenu(**{"title": "Красные вина", "description": "Дли романтического вечера"})
        submenu_2_1.owner = menu_2.id
        submenu_2_1.dishes_count = 3
        await self.crud.add_to_db(submenu_2_1)
        dish_2_1_1: Dish = Dish(
            **{"title": "Шемен де Пап ля", "description": "Вино красное - фруктовое", "price": "2700.93"},
        )
        dish_2_1_1.owner = submenu_2_1.id
        dish_2_1_2: Dish = Dish(
            **{"title": "Рипароссо Монтепул", "description": "Вино красное - сухое", "price": "3100.23"},
        )
        dish_2_1_2.owner = submenu_2_1.id
        dish_2_1_3: Dish = Dish(
            **{"title": "Кьянти", "description": "Вино красное - элегантное, комплексное", "price": "1523.37"},
        )
        dish_2_1_3.owner = submenu_2_1.id
        await self.crud.add_to_db(dish_2_1_1)
        await self.crud.add_to_db(dish_2_1_2)
        await self.crud.add_to_db(dish_2_1_3)
        submenu_2_2: SubMenu = SubMenu(**{"title": "Виски", "description": "Для интересных бесед"})
        submenu_2_2.owner = menu_2.id
        submenu_2_2.dishes_count = 3
        await self.crud.add_to_db(submenu_2_2)
        dish_2_2_1: Dish = Dish(
            **{
                "title": "Джемисон",
                "description": "Классический купажированный виски, 4х летней выдержки",
                "price": "540.22",
            },
        )
        dish_2_2_1.owner = submenu_2_2.id
        dish_2_2_2: Dish = Dish(
            **{
                "title": "Джек Дениелс",
                "description": "Характерен мяглкий вкус, сочетает в себе карамельно-ванильные и древесные нотки",
                "price": "697.11",
            },
        )
        dish_2_2_2.owner = submenu_2_2.id

        dish_2_2_3: Dish = Dish(
            **{
                "title": "Чивас Ригал",
                "description": "Это купаж высококачественных солодовых и зерновых виски, выдержанный"
                " как минимум в течение 12 лет",
                "price": "750.25",
            },
        )
        dish_2_2_3.owner = submenu_2_2.id
        await self.crud.add_to_db(dish_2_2_1)
        await self.crud.add_to_db(dish_2_2_2)
        await self.crud.add_to_db(dish_2_2_3)
        return {"FULL_MENU": "SUCCESSFULLY CREATED"}

    async def make_excel_file(self):
        print("MAKING FILE")
        q = """SELECT menu.id, menu.title, menu.description, submenu.id as sb_id,
            submenu.title as sb_title, submenu.description as sb_description, dish.id as dsh_id,
            dish.title as dsh_title, dish.description as dsh_description, dish.price
            FROM menu JOIN submenu ON submenu.owner = menu.id JOIN dish ON dish.owner = submenu.id"""
        data = await self.db.execute(q)
        d = data.fetchall()

        d_ser = [list(dict(el).values()) for el in d]
        lst = copy.deepcopy(d_ser)
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                if i != 0:
                    if lst[i][j] == lst[i - 1][j]:
                        lst[i][j] = ""
                if lst[i - 1][j] == "" and lst[i][j] == d_ser[i - 1][j]:
                    lst[i][j] = ""
        return lst


def get_full_menu(
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_redis),
) -> FullMenu:
    crud: CRUD = CRUD(db)
    return FullMenu(crud=crud, cache=cache)
