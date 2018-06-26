# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class OpenAcademy(models.Model):

    _name = 'openacademy.course'
    _rec_name = 'name'

    name = fields.Char(string='Course', help='Course Name', required='True')
    description = fields.Text(string='Description')

    responsible_id = fields.Many2one('res.users', ondelete='set null', string='Responsible', index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string='Sessions')

    _sql_constraints = [('name_description_check',
                         'CHECK(name != description)',
                         'The title of the course should not be the description'),

                        ('unique_name',
                         'UNIQUE(name)',
                         'The course title should be unique')
                        ]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(OpenAcademy, self).copy(default)


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char()
    start_date = fields.Datetime(string='Start Date')
    duration = fields.Float(digits=(6, 2), help='Duration in Days')
    seats = fields.Integer(string='Number of Seats')

    instructor_id = fields.Many2one('res.partner', string='Instructor')
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string='Course', required='True',
                                help='Session Courses')
    attendee_ids = fields.Many2many('res.partner', string='Attendees')
    active = fields.Boolean(string='Active', default=True)
    taken_seats = fields.Float(string='Taken Seats', compute='_compute_taken', store=True)
    attendees_count = fields.Float(string='Attendees Count', compute='_compute_attendees_count', store=True)
    color = fields.Integer()

    @api.depends('attendee_ids')
    def _compute_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendee_ids)

    # @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect seats value",
                    'message': "Cannot give negative seat number",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Too many people attending the session. Not Enough Seats"
                }
            }

    @api.depends('seats', 'attendee_ids')
    def _compute_taken(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0.0
            else:
                record.taken_seats = len(record.attendee_ids)/record.seats*100.0
            return record.taken_seats

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_attendee(self):
        for record in self:
            if record.instructor_id in record.attendee_ids:
                raise exceptions.ValidationError("A session instructor cannot be an attendee")

