# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FieldList, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, Regexp, DataRequired, NumberRange
from wtforms import ValidationError

from ..models import Region
from ..constants import MAX_LENGTH, REG_EXP_PHONE


class RecycleOrderForm(Form):
    service_type = SelectField('服务方式', coerce=int, validators=[DataRequired()], choices=[
        (0, '请选择服务方式'),
        (1, '上门服务'),
        (2, '邮寄服务'),
    ])
    fullname = StringField('姓名', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['fullname'], '长度不合法'),
        Regexp('[\u4e00-\u9fa5]+$', message='真实姓名中不能包含除简体汉字之外的字符')
    ])
    cellphone = StringField('手机号', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['cellphone'], '长度不合法'),
        Regexp(REG_EXP_PHONE, message='无效的手机号码')
    ])
    province = SelectField('省份', coerce=int, validators=[DataRequired()])
    city = SelectField('城市', coerce=int, validators=[DataRequired()])
    county = SelectField('县区', coerce=int)
    address = TextAreaField('详细地址', validators=[InputRequired()])
    remark = TextAreaField('备注')
    submit = SubmitField('提交')

    def validate_city(self, field):
        region = Region.query.get(field.data)
        if not region or region.parent_id != self.province.data:
            raise ValidationError('请重新选择')

    def validate_county(self, field):
        if len(self.county.choices) > 1:
            if not field.data:
                raise ValidationError('请选择县区')
            else:
                region = Region.query.get(field.data)
                if not region or region.parent_id != self.city.data:
                    raise ValidationError('请重新选择')
