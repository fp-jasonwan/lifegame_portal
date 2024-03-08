from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from booth.models import BoothTraffic, Booth
from player.models import Player
from django.utils.crypto import get_random_string
# Create your models here.

booth_choices = (('G1 銀行', 'G1 銀行'),
('G2 監獄', 'G2 監獄'),
('G3 醫院', 'G3 醫院'),
('G4 公園', 'G4 公園'),
('G5 稅局', 'G5 稅局'),
('G6 法院', 'G6 法院'),
('G7 警局', 'G7 警局'),
('G8 社署', 'G8 社署'),
('S1 小學及中學', 'S1 小學及中學'),
('S2 大學', 'S2 大學'),
('S3 身心靈學院', 'S3 身心靈學院'),
('W1 職業培訓中心', 'W1 職業培訓中心'),
('W2 報館', 'W2 報館'),
('W3 健身室', 'W3 健身室'),
('W4 語言中心', 'W4 語言中心'),
('W5 物理治療診所', 'W5 物理治療診所'),
('W6 律師樓', 'W6 律師樓'),
('W7 酒店', 'W7 酒店'),
('W8 幼兒中心', 'W8 幼兒中心'),
('W9 航空公司', 'W9 航空公司'),
('C1 黑社會', 'C1 黑社會'),
('C2 股票交易所', 'C2 股票交易所'),
('C3 虛擬貨幣交易所', 'C3 虛擬貨幣交易所'),
('C4 地產公司', 'C4 地產公司'),
('C5 選舉投票站', 'C5 選舉投票站'),
('C6 社區中心', 'C6 社區中心'),
('C7 信貸公司', 'C7 信貸公司'),
('C8 創業中心', 'C8 創業中心'),
('C9 保險公司', 'C9 保險公司'),
('E1 賭場', 'E1 賭場'),
('E2 酒吧', 'E2 酒吧'),
('E3 卡拉OK', 'E3 卡拉OK'),
('E4 兼職情人', 'E4 兼職情人'),
('R1 婚姻註冊處', 'R1 婚姻註冊處'),
('R2 家庭', 'R2 家庭'),
('R3 友情', 'R3 友情'),
('R4 生死教育', 'R4 生死教育'),
('R5 交友app', 'R5 交友app'),
('R6 情緒教育', 'R6 情緒教育'),
('R7 一夜情', 'R7 一夜情'),
('A1 義工', 'A1 義工'),
)

def generate_encrypted_string():
    return get_random_string(32)

class User(AbstractUser):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{}{} - {} {}".format('{:03d}'.format(self.id), self.school_code, self.last_name, self.first_name)

    def is_oc(self):
        return self.user_type in ('oc', 'admin')

    def is_player(self):
        return Player.objects.filter(user=self).exists()

    def get_player(self):
        return Player.objects.filter(user=self, active=True).first()

    def get_instructor_group(self):
        if self.user_type == 'student':
            grp = InstructorGroup.objects.filter(students=self).first()
            if grp: 
                return grp.id
        elif self.user_type == 'instructor':
            grp = InstructorGroup.objects.filter(instructor=self).first()
            if grp:
                return grp.id
        return ""

    def get_id(self):
        instructor_group_id = self.get_instructor_group()
        if instructor_group_id:
            return f"{self.id:03d}"
        else:
            return f"{self.id:03d}"

    @property
    def player(self):
        return Player.objects.filter(
            user=self,
            active=True
        ).first()

    @property
    def full_id(self):
        return self.get_id()

    user_type = models.CharField(
        max_length=10,
        choices=(('student', 'student'), ('oc', 'oc'),('admin', 'admin'), ('instructor', 'instructor'),
                 ('vip', 'vip')),
        blank=True, null=True
        )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True )
    school = models.CharField(max_length=100, blank=True, null=True)
    encrypted_id = models.CharField(max_length=32, default=generate_encrypted_string)
    school_code = models.CharField(max_length=2, blank=True, null=True)
    best_booth = models.CharField(
        max_length=50, 
        choices=booth_choices,
        blank=True, 
        null=True
    )
    room_no = models.CharField(max_length=50, blank=True, null=True)
    
class InstructorGroup(models.Model):
    def get_player(self):
        players = Player.objects.filter(user__in=self.students.all()).order_by('-active','user__id')
        return players
    id = models.AutoField(primary_key=True)
    instructor = models.ManyToManyField('account.User', related_name='instructor')
    students = models.ManyToManyField('account.User', related_name='student')