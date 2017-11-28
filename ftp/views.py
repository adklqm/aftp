# encoding: utf-8

def get_view_by_group_index(window, group, index):
    return window.views_in_group(group)[index]


def get_all_views(window):
    views = window.views()
    active_view = window.active_view()
    if active_view and active_view.id() not in (lambda .0: continue[ view.id() for view in .0 ])(views):
        views.append(active_view)
    return views