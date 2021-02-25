from portal.models import NavMenu

parent_sidebar_id_tag = {'Home': 'fa-chart-pie',
                         'Usage Reports': 'fa-align-left',
                         'Invoices': 'fa-envelope-open',
                         'Default': 'fa-copy'}
sub_menu_url = {'Default': 'index',
                2: 'dashboard',
                7: 'dashboard',
                8: 'dashboard',
                9: 'dashboard',
                10: 'dashboard',
                11: 'dashboard',
                12: 'dashboard',
                13: 'dashboard',
                17: 'invoices',
                18: 'invoices',
                19: 'invoices',
                20: 'invoices',
                21: 'invoices',
                22: 'invoices',
                23: 'invoices',
                24: 'payment',
                26: 'payment'}  # menu_id, url_name


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
        _sub_menu = navs.filter(parent_menu_id=parant.menu_id, is_visible=True).order_by('sort_index')
        _r_parent = {'caption': parant.caption,
                     'icon_tag': parent_sidebar_id_tag[parant.caption] if parant.caption in parent_sidebar_id_tag else parent_sidebar_id_tag['Default'],
                     'is_enable': parant.is_enable
                     }
        _r_sub_menu = list()
        for sub in _sub_menu:
            _r_sub_menu.append({'menu_id': sub.menu_id,
                                'caption': sub.caption,
                                'url': sub_menu_url[sub.menu_id] if sub.menu_id in sub_menu_url else sub_menu_url['Default'],
                                'is_enable': sub.is_enable
                                })
        _nav = (_r_parent, _r_sub_menu)
        sidebar_menu.append(_nav)
    return sidebar_menu


