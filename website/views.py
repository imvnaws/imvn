from flask import Blueprint, render_template, request, flash, redirect, url_for, json
from datetime import datetime, date
from .entity import Entity
import datetime
import json
views = Blueprint('views', __name__)

@views.route('/')
def home():
    contact = Entity.create()
    result = contact.read()
    contact.info(result)
    return render_template('index.html', contacts=result)

@views.route('/addContact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        dob = datetime.datetime.strptime(request.form.get('dob'), '%Y-%m-%d')
        arg = {
            "firstName" : firstName,
            "lastName" : lastName,
            "dob" : dob
        }
    
        if not firstName :
            flash('First name is required.', category='warning')
        elif not lastName:
            flash('Last name is required.', category='warning')
        #elif dob > date.today():
            #flash('Date of birth must be earlier than the current date.', category='warning')
        else:
            newContact = Entity.create(arg)
            newContact.commit()
            flash('Contact has been added.', category='success')
            return redirect(url_for('views.home'))

    return render_template('addContact.html')

@views.route('/<contact_id>')
def viewContact(contact_id):
    this = Entity()
    contact = this.read("id = " + contact_id)
    if contact:
        return render_template('contact.html', contact=contact[0])
    else:
        flash('Contact ' + contact_id + ' not found.', category='warning')
        return redirect(url_for('views.home'))

@views.route('/<int:contact_id>/editContact', methods=('GET', 'POST'))
def editContact(contact_id):
    contacts = ()
    this = Entity()
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        dob = datetime.datetime.strptime(request.form.get('dob'), '%Y-%m-%d')
        arg = {
            "id" : contact_id,
            "firstName" : firstName,
            "lastName" : lastName,
            "dob" : dob,
            "editTime" : datetime.datetime.now()
        }
    
        if not firstName :
            flash('First name is required.', category='warning')
        elif not lastName:
            flash('Last name is required.', category='warning')
        #elif dob > date.today():
            #flash('Date of birth must be earlier than the current date.', category='warning')
        else:
            updatedContact = Entity()
            updatedContact.update(arg)
            updatedContact.debug("Double checking")
            updatedContact.debug(updatedContact.id)
            updatedContact.debug(updatedContact)
            updatedContact.info("Commit started")
            updatedContact.commit()
            updatedContact.info("Commit done")
            flash('Contact has been updated.', category='success')
            return redirect(url_for('views.viewContact', contact_id=updatedContact.id))
        this = Entity()
    contacts = this.read("id = " + str(contact_id))
    contact = contacts[0]
    if contact:
        return render_template('editContact.html', contact=contact)
    else:
        flash('Contact ' + contact_id + ' not found.', category='warning')
        return redirect(url_for('views.home'))

@views.route('/delete-contact', methods=['POST'])
def delete_contact():
    this = Entity()
    this.debug('Entering Delete Statement')
    note = json.loads(request.data)
    this.debug(note)
    contactId = note['contactId']
    contact = this.read("id = " + str(contactId))
    this.debug(contact)
    if contact:
        this.deleteById(contactId)
    return redirect(url_for('views.home'))