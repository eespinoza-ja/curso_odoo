# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError
from psycopg2 import IntegrityError
from openerp.tools import mute_logger

class GlobalTestOpenAcademyCourse(TransactionCase):
    #Seudo-constructor test setUp Method
    def setUp(self):
        #Define global variables to test methods
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.variable = 'Hello World'
        self.course = self.env['openacademy.course']

    #Class Methods
    def create_course(self, course_name, course_description, course_responsible_id):
        course_id = self.course.create({
            'name': course_name,
            'description': course_description,
            'responsible_id': course_responsible_id
        })
        return course_id

    #Test Methods
    @mute_logger('odoo.sql_db')
    def test_01_name_equal_description(self):
        '''
        Test to create a course with the same name and description
        '''
        with self.assertRaisesRegexp(IntegrityError,
                                     'new row for relation "openacademy_course" violates check constraint '
                                     '"openacademy_course_name_description_check'):
            self.create_course('test','test',None)

    @mute_logger('odoo.sql_db')
    def test_02_same_name_other_course(self):
        '''
        Test to create a course with the same name as other course
        '''
        with self.assertRaisesRegexp(IntegrityError,
                                     'duplicate key value violates unique constraint '
                                     '"openacademy_course_name_unique"'):
            self.create_course('Course 001','test1',None)

    def test_03_duplicate_course(self):
        '''
        Test to duplicate a course
        '''
        course = self.env.ref('openacademy.course0')
        course_id = course.copy()
        print("course_id: "+course_id)