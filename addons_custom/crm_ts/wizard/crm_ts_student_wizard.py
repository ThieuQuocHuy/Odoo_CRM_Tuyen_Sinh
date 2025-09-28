# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import random


class CrmTsStudentWizard(models.TransientModel):
    _name = 'crm_ts.student.wizard'
    _description = 'Student Management Wizard'

    lead_id = fields.Many2one('crm_ts.lead', string='Lead', required=True)
    lead_name = fields.Char(string='Lead Name', readonly=True)
    student_name = fields.Char(string='Tên học sinh')
    identifier_code = fields.Char(string='Mã định danh', readonly=True)
    birth_date = fields.Date(string='Ngày sinh')
    lead_birth_year = fields.Char(string='Năm sinh')
    
    action_type = fields.Selection([
        ('create_new', 'Tạo học sinh mới'),
        ('link_existing', 'Liên kết với học sinh'),
        ('unlink', 'Hủy liên kết với học sinh')
    ], string='Hành động', default='create_new', required=True)
    
    student_id = fields.Many2one('crm_ts.lead', string='Học sinh Liên kết', 
                                 domain="[('type', '=', 'opportunity'), ('identifier_code', '!=', False)]")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'lead_id' in self.env.context:
            lead_id = self.env.context['lead_id']
            lead = self.env['crm_ts.lead'].browse(lead_id)
            # Tạo random mã định danh
            random_code = str(random.randint(100000, 999999))
            res.update({
                'lead_id': lead_id,
                'lead_name': lead.name,
                'student_name': lead.student_name,
                'identifier_code': random_code,
                'birth_date': lead.birth_date,
                'lead_birth_year': lead.lead_birth_year,
            })
        return res

    def action_confirm(self):
        self.ensure_one()
        lead = self.lead_id
        
        if self.action_type == 'create_new':
            # Tạo học sinh mới với mã random
            if not self.student_name or not self.lead_birth_year:
                raise UserError(_('Vui lòng nhập đủ Tên học sinh và Năm sinh.'))
            
            # Kiểm tra trùng lặp mã định danh
            duplicate = self.env['crm_ts.lead'].search_count([
                ('id', '!=', lead.id),
                ('identifier_code', '=', self.identifier_code)
            ])
            if duplicate:
                # Tạo mã mới nếu trùng
                self.identifier_code = str(random.randint(100000, 999999))
            
            # Cập nhật thông tin học sinh
            lead.write({
                'student_name': self.student_name,
                'identifier_code': self.identifier_code,
                'birth_date': self.birth_date,
                'lead_birth_year': self.lead_birth_year,
                'student_mode': True,
            })
            
            # Thông báo thành công
            pass
            
        elif self.action_type == 'link_existing':
            if not self.student_id:
                raise UserError(_('Vui lòng chọn học sinh để liên kết.'))
            
            # Kiểm tra xem học sinh đã được liên kết với lead khác chưa
            existing_link = self.env['crm_ts.lead'].search([
                ('id', '!=', lead.id),
                ('identifier_code', '=', self.student_id.identifier_code)
            ])
            if existing_link:
                raise UserError(_('Học sinh này đã được liên kết với lead khác: %s') % existing_link.name)
            
            # Logic liên kết học sinh
            lead.write({
                'student_name': self.student_id.student_name,
                'identifier_code': self.student_id.identifier_code,
                'birth_date': self.student_id.birth_date,
                'lead_birth_year': self.student_id.lead_birth_year,
                'student_mode': True,
            })
            # Thông báo liên kết thành công
            pass
            
        elif self.action_type == 'unlink':
            # Logic hủy liên kết - chỉ reset student_mode, giữ lại thông tin để có thể liên kết lại
            lead.write({
                'student_mode': False,
            })
            # Thông báo hủy liên kết thành công
            pass

        # Đóng popup và mở lại form lead để hiển thị mã định danh
        return {
            'type': 'ir.actions.act_window',
            'name': _('Học sinh'),
            'res_model': 'crm_ts.lead',
            'view_mode': 'form',
            'res_id': lead.id,
            'target': 'current',
            'context': dict(self.env.context),
        }
