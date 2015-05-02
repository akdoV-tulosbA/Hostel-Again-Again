# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Welcome to the IIIT Hostel Portal!")
    return dict(message=T('Hello World'))


@auth.requires_login()
def hello():
    return dict(message='hello %(first_name)s' % auth.user)


#def register():
 #   admin_auth = session.auth
  #  auth.is_logged_in = lambda: False
   # def post_register(form):
    #    session.auth = admin_auth
    #    auth.user = session.auth.user
    #auth.settings.register_onaccept = post_register
    #return dict(form=auth.register())

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@auth.requires_login()
def newspaper():
    db.newspaper.subscriber.default=auth.user.id
    x = db(db.newspaper.subscriber.default==auth.user.id).select(db.newspaper.id)
    form=SQLFORM(db.newspaper).process()
    id = form.vars.id
    if form.accepted:
        redirect(URL('default', 'remember', args=[id]))
        session.flash = ('Okay!')
    return locals() 


@auth.requires_login()
def remember():
    id = request.args(0)
    return locals()


@auth.requires_login()
def pre_del():
    form = SQLFORM.factory(Field('enter_id', requires=IS_NOT_EMPTY()))
    if form.process().accepted:
        query = (db.newspaper.subscriber==auth.user.id and db.newspaper.id==form.vars.enter_id)
        x = db(query).count()
        db(query).delete()
        if x > 0:
            session.flash = "Record Deleted!"
        else:
            session.flash = "No such record!"
        redirect(URL('default', 'show_newspaper_subscriptions'))
    return locals()

@auth.requires_login()
def del_old_subscriptions():
    form = SQLFORM(db.newspaper).process


@auth.requires_login()
def show_newspaper_subscriptions():
    subs = db(db.newspaper.subscriber==auth.user.id).select(db.newspaper.id, db.newspaper.choice_of_newspaper, db.newspaper.subscription_type) 
    return locals()

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def already_got_room():
    message = "Error! User already registered for another room."
    #response.flash = "User already registered"
    return locals()


@auth.requires_login()
def room_year():
    j = (db(db.ug2k15.student==auth.user.id).count() +
         db(db.ug2k14.student==auth.user.id).count() +
         db(db.ug2k13.student==auth.user.id).count() +
         db(db.fug2k15.student==auth.user.id).count() +
         db(db.fug2k14.student==auth.user.id).count() +
         db(db.fug2k13.student==auth.user.id).count() +
         db(db.pg2k15.student==auth.user.id).count() +
         db(db.pg2k14.student==auth.user.id).count())
    i = db(db.room_year.student==auth.user.id).count()
    if j == 0:
        db(db.room_year.student == auth.user.id).delete()
    elif i > 0:
        session.flash = "You have already registered."
        redirect(URL('default', 'already_got_room'))
    db.room_year.student.default=auth.user.id
    form=SQLFORM(db.room_year).process()
    if form.vars.batch  ==  'UG2K15':
        if auth.user.sex == 'Female':
            redirect(URL('default', 'FUG2K15', args=["Parul", "Nivas", 1]))
        else:
            redirect(URL('default', 'UG2K15', args=["Palash", "Nivas", 1]))


    elif form.vars.batch  ==  'UG2K14':
        if auth.user.sex == 'Female':
            redirect(URL('default', 'FUG2K14', args=["Parul", "Nivas", 1]))
        else:
            redirect(URL('default', 'UG2K14', args=["Palash", "Nivas", 1]))


    elif form.vars.batch  ==  'UG2K13 and before':
        if auth.user.sex == 'Female':
            redirect(URL('default', 'FUG2K13', args=["Parijaat", "Nivas", 1]))
        else:
            redirect(URL('default', 'UG2K13', args=["Palash", "Nivas", 1]))

    elif form.vars.batch  ==  'PG2K15':
        if auth.user.sex == 'Female':
            redirect(URL('default', 'FUG2K15', args=["Parul", "Nivas", 1]))
        else:
            redirect(URL('default', 'PG2K15', args=["Bakul", "Nivas", 1]))

    elif form.vars.batch  ==  'PG2K14 and before':
        if auth.user.sex == 'Female':
            redirect(URL('default', 'FUG2K14', args=["Parul", "Nivas", 1]))
        else:
            redirect(URL('default', 'PG2K14', args=["Bakul", "Nivas", 1]))
    return locals()


@auth.requires_login()
def UG2K15():
    hname = request.args
    i = db(db.ug2k15.student==auth.user.id).count()
    if i > 0:
        session.flash = "You have already registered."
        redirect(URL('default', 'already_got_room'))

    db.ug2k15.student.default=auth.user.id
    db.ug2k15.student.requires= IS_NOT_IN_DB(db, db.ug2k15.student)
    form = SQLFORM(db.ug2k15).process()
    count = db(db.ug2k15.room_number == form.vars.room_number).count()
    if count > 2:
        message = "This room already has two occupants."
        db(db.ug2k15.student == auth.user.id).delete()
        db(db.room_year.student == auth.user.id).delete()
        session.flash = message
        redirect(URL('default', 'two_people'))
    elif form.accepted:
        session.flash = "Registered!"
        redirect(URL('default', 'index'))
    return locals()


@auth.requires_login()
def PG2K15():
    hname = request.args
    i = db(db.pg2k15.student==auth.user.id).count()
    if i > 0:
        session.flash = "You have already registered."
        redirect(URL('default', 'already_got_room'))

    db.pg2k15.student.default=auth.user.id
    db.pg2k15.student.requires= IS_NOT_IN_DB(db, db.pg2k15.student)
    form = SQLFORM(db.pg2k15).process()
    count = db(db.pg2k15.room_number == form.vars.room_number).count()
    if count > 2:
        message = "This room already has two occupants."
        db(db.pg2k15.student == auth.user.id).delete()
        db(db.room_year.student == auth.user.id).delete()
        session.flash = message
        redirect(URL('default', 'two_people'))
    elif form.accepted:
        session.flash = "Registered!"
        redirect(URL('default', 'index'))
    return locals()


@auth.requires_login()
def FUG2K15():
    hname = request.args
    i = db(db.fug2k15.student==auth.user.id).count()
    if i > 0:
        session.flash = "You have already registered."
        redirect(URL('default', 'already_got_room'))

    db.fug2k15.student.default=auth.user.id
    db.fug2k15.student.requires= IS_NOT_IN_DB(db, db.fug2k15.student)
    form = SQLFORM(db.fug2k15).process()
    count = db(db.fug2k15.room_number == form.vars.room_number).count()
    if count > 2:
        message = "This room already has two occupants."
        db(db.fug2k15.student == auth.user.id).delete()
        db(db.room_year.student == auth.user.id).delete()
        session.flash = message
        redirect(URL('default', 'two_people'))
    elif form.accepted:
        session.flash = "Registered!"
        redirect(URL('default', 'index'))
    return locals()


@auth.requires_login()
def UG2K14():
    hname = request.args
    i = db(db.ug2k14.student==auth.user.id).count()
    if i > 0:
        session.flash = "You have already registered."
        redirect(URL('default', 'already_got_room'))

    db.ug2k14.student.default=auth.user.id
    db.ug2k14.student.requires= IS_NOT_IN_DB(db, db.ug2k14.student)
    form = SQLFORM(db.ug2k14).process()
    count = db(db.ug2k14.room_number == form.vars.room_number).count()
    if count > 1:
        message = "This room already has an occupant."
        db(db.ug2k14.student == auth.user.id).delete()
        db(db.room_year.student == auth.user.id).delete()
        session.flash = message
        redirect(URL('default', 'people'))
    elif form.accepted:
        session.flash = "Registered!"
        redirect(URL('default', 'index'))
    return locals()


@auth.requires_login()
def PG2K14():
    hname = request.args
    i = db(db.pg2k14.student==auth.user.id).count()
    if i > 0:
        session.flash = "You have already registered."
        redirect(URL('default', 'already_got_room'))

    db.pg2k14.student.default=auth.user.id
    db.pg2k14.student.requires= IS_NOT_IN_DB(db, db.pg2k14.student)
    form = SQLFORM(db.pg2k14).process()
    count = db(db.pg2k14.room_number == form.vars.room_number).count()
    if count > 1:
        message = "This room already has an occupant."
        db(db.pg2k14.student == auth.user.id).delete()
        db(db.room_year.student == auth.user.id).delete()
        session.flash = message
        redirect(URL('default', 'people'))
    elif form.accepted:
        session.flash = "Registered!"
        redirect(URL('default', 'index'))
    return locals()


@auth.requires_login()
def FUG2K14():
    hname = request.args
    i = db(db.fug2k14.student==auth.user.id).count()
    if i > 0:
        session.flash = "You have already registered."
        redirect(URL('default', 'already_got_room'))

    db.fug2k14.student.default=auth.user.id
    db.fug2k14.student.requires= IS_NOT_IN_DB(db, db.fug2k14.student)
    form = SQLFORM(db.fug2k14).process()
    count = db(db.fug2k14.room_number == form.vars.room_number).count()
    if count > 1:
        message = "This room already has an occupant."
        db(db.fug2k14.student == auth.user.id).delete()
        db(db.room_year.student == auth.user.id).delete()
        session.flash = message
        redirect(URL('default', 'people'))
    elif form.accepted:
        session.flash = "Registered!"
        redirect(URL('default', 'index'))
    return locals()



@auth.requires_login()
def UG2K13():
    hname = request.args
    i = db(db.ug2k13.student==auth.user.id).count()
    if i > 0:
        session.flash = "You have already registered."
        redirect(URL('default', 'already_got_room'))

    db.ug2k13.student.default=auth.user.id
    db.ug2k13.student.requires= IS_NOT_IN_DB(db, db.ug2k13.student)
    form = SQLFORM(db.ug2k13).process()
    count = db(db.ug2k13.room_number == form.vars.room_number).count()
    if count > 1:
        message = "This room already has an occupant."
        db(db.ug2k13.student == auth.user.id).delete()
        db(db.room_year.student == auth.user.id).delete()
        session.flash = message
        redirect(URL('default', 'people'))
    elif form.accepted:
        session.flash = "Registered!"
        redirect(URL('default', 'index'))
    return locals()


@auth.requires_login()
def FUG2K13():
    hname = request.args
    i = db(db.fug2k13.student==auth.user.id).count()
    if i > 0:
        session.flash = "You have already registered."
        redirect(URL('default', 'already_got_room'))

    db.fug2k13.student.default=auth.user.id
    db.fug2k13.student.requires= IS_NOT_IN_DB(db, db.fug2k13.student)
    form = SQLFORM(db.fug2k13).process()
    count = db(db.fug2k13.room_number == form.vars.room_number).count()
    if count > 1:
        message = "This room already has an occupant."
        db(db.fug2k13.student == auth.user.id).delete()
        db(db.room_year.student == auth.user.id).delete()
        session.flash = message
        redirect(URL('default', 'people'))
    elif form.accepted:
        session.flash = "Registered!"
        redirect(URL('default', 'index'))
    return locals()


@auth.requires_login()
def two_people():
    message = "Sorry! Two people already registered for this room."
    return locals()


@auth.requires_login()
def people():
    message = "This room is occupied."
    return locals()
