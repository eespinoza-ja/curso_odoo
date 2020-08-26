# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError
from psycopg2 import IntegrityError
from openerp.tools import mute_logger

class GlobalTestOpenAcademySession(TransactionCase):
    #Seudo-constructor test setUp Method
    def setUp(self):
        #Define global variables to test methods
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']

    #Test Methods
    def test_01_session_attende_is_instructor(self):
        '''
        Test to create a session with an attende as instructor
        '''
        partner = self.env.ref('base.res_partner_12')
        with self.assertRaisesRegexp(ValidationError,
                                     "A session's instructor can't be an attendee"):
            session_id = self.session.create({
                'name': 'Session01',
                'seats': 1,
                'instructor_id': partner.id,
                'attendee_ids': [partner.id],
                'course_id' : self.env.ref('openacademy.course1').id
            })

    @mute_logger('odoo.sql_db')
    def test_02_session_without_course(self):
        '''
        Test to create a session without a course
        '''
        partner = self.env.ref('base.res_partner_12')
        with self.assertRaisesRegexp(IntegrityError,
                                     'null value in column "course_id" violates not-null constraint'):
            session_id = self.session.create({
                'name': 'Session01',
                'seats': 1,
                'instructor_id': partner.id,
                'attendee_ids': [partner.id],
                'course_id': None
            })

    def test_03_session_workflow(self):
        '''
        Test to create a session workflow
        '''
        partner = self.env.ref('base.res_partner_12')
        partner_1 = self.env.ref('base.res_partner_address_15')
        session_id = self.session.create({
            'name': 'Session01',
            'seats': 1,
            'instructor_id': partner.id,
            'attendee_ids': [partner_1.id],
            'course_id': self.env.ref('openacademy.course1').id
        })