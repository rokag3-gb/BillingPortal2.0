from portal.models import NavMenu


def get_sidebar_menu():
    # TODO: 유저별로 사용 vendor같은 사용가능한 메뉴만 보이게 return.
    # TODO: 2월 마일스톤은 우선 전 메뉴 가능하도록.
    # 2 Depth
    # [(parent_menu, (nav_menus, ),
    #   (parent_menu, (nav_menus, ),
    #   ...
    #   )]
    sidebar_menu = list()
    navs = NavMenu.objects.all()
    parent_menu_list = navs.filter(parent_menu_id=None).order_by('menu_id')
    for parant in parent_menu_list:
        _sub_menu = navs.filter(parent_menu_id=parant.menu_id).order_by('sort_index')
        _nav = (parant.menu_name, tuple(i.menu_name.rstrip('\r\n') for i in _sub_menu))
        sidebar_menu.append(_nav)
    print('navbar 호출')
    return sidebar_menu
