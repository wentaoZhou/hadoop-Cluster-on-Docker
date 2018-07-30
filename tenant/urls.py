from django.conf.urls import url
from tenant.controller.login import login, loginForm, register, registerForm
from tenant.controller.index import index, welcome
from tenant.controller.tenant import tenant, tenantManage, tenantUser, getTenantUser, addTenant, monitorTenant, getaddTenantList
from tenant.controller.ajaxToGetData import puyTenant, ajaxToGetTenantInfo, ajaxToGetTenant, ajaxToGetAllTenantStatus, ajaxToGetAddMember

from tenant.controller.userInfo import userinfo
from tenant.controller.operaterCluster import addContainer
from tenant.controller.operaterCluster import deleteNode
from tenant.hadoopConfig.operateHadoop import startHadoop
from tenant.hadoopConfig.operateHadoop import stopHadoop
urlpatterns = [
    url('login/', login),
    url('loginForm/', loginForm),
    url('register/', register),
    url('registerForm/', registerForm),

    url('index/', index),
    url('welcome/', welcome),

    url('tenant/', tenant),
    url('tenantManage/', tenantManage),
    url('tenantUser/', tenantUser),
    url('getTenantUser/', getTenantUser),
    url('addTenant/', addTenant),
    url('monitorTenant/', monitorTenant),
    url('getaddTenantList/', getaddTenantList),


    # 购买集群，获取数据
    url('puyTenant/', puyTenant),
    url('ajaxToGetTenantInfo/', ajaxToGetTenantInfo),
    url('ajaxToGetTenant/', ajaxToGetTenant),
    url('ajaxToGetAllTenantStatus/', ajaxToGetAllTenantStatus),
    url('ajaxToGetAddMember/', ajaxToGetAddMember),


    url('userinfo/', userinfo),
    # 增加，删除节点
    url('addContainer',addContainer),
    url('deleteNode',deleteNode),

    # 启动关闭集群
    url('startHadoop',startHadoop),
    url('stopHadoop',stopHadoop)
]
