# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
  import json
except ImportError:
  import simplejson as json

from cm_api.endpoints.types import config_to_json, json_to_config, \
    ApiList, BaseApiObject
from cm_api.endpoints.roles import ApiRole

__docformat__ = "epytext"

ROLE_CONFIG_GROUPS_PATH = "/clusters/%s/services/%s/roleConfigGroups"
CM_ROLE_CONFIG_GROUPS_PATH = "/cm/service/roleConfigGroups"

def _get_role_config_groups_path(cluster_name, service_name):
  if cluster_name:
    return ROLE_CONFIG_GROUPS_PATH % (cluster_name, service_name)
  else:
    return CM_ROLE_CONFIG_GROUPS_PATH

def _get_role_config_group_path(cluster_name, service_name, name):
  path = _get_role_config_groups_path(cluster_name, service_name)
  return "%s/%s" % (path, name)

def create_role_config_groups(resource_root, service_name, apigroup_list,
    cluster_name="default"):
  """
  Create role config groups.
  @param resource_root: The root Resource object.
  @param service_name: Service name.
  @param apigroup_list: List of role config groups to create.
  @param cluster_name: Cluster name.
  @return: New ApiRoleConfigGroup object.
  """
  body = json.dumps(apigroup_list.to_json_dict())
  resp = resource_root.post(_get_role_config_groups_path(
      cluster_name, service_name), data=body)
  return ApiList.from_json_dict(ApiRoleConfigGroup, resp, resource_root)

def create_role_config_group(resource_root, service_name, name, display_name,
    role_type, cluster_name="default"):
  """
  Create a role config group.
  @param resource_root: The root Resource object.
  @param service_name: Service name.
  @param name: The name of the new group.
  @param display_name: The display name of the new group.
  @param role_type: The role type of the new group.
  @param cluster_name: Cluster name.
  @return: List of created role config groups.
  """
  apigroup = ApiRoleConfigGroup(resource_root, name, display_name, role_type)
  apigroup_list = ApiList([apigroup])
  return create_role_config_groups(resource_root, service_name, apigroup_list,
      cluster_name)[0]

def get_role_config_group(resource_root, service_name, name,
    cluster_name="default"):
  """
  Find a role config group by name.
  @param resource_root: The root Resource object.
  @param service_name: Service name.
  @param name: Role config group name.
  @param cluster_name: Cluster name.
  @return: An ApiRoleConfigGroup object.
  """
  return _get_role_config_group(resource_root, _get_role_config_group_path(
      cluster_name, service_name, name))

def _get_role_config_group(resource_root, path):
  dic = resource_root.get(path)
  return ApiRoleConfigGroup.from_json_dict(dic, resource_root)

def get_all_role_config_groups(resource_root, service_name,
    cluster_name="default"):
  """
  Get all role config groups in the specified service.
  @param resource_root: The root Resource object.
  @param service_name: Service name.
  @param cluster_name: Cluster name.
  @return: A list of ApiRoleConfigGroup objects.
  """
  dic = resource_root.get(_get_role_config_groups_path(
      cluster_name, service_name))
  return ApiList.from_json_dict(ApiRoleConfigGroup, dic, resource_root)

def update_role_config_group(resource_root, service_name, name, apigroup,
    cluster_name="default"):
  """
  Update a role config group by name.
  @param resource_root: The root Resource object.
  @param service_name: Service name.
  @param name: Role config group name.
  @param apigroup: The updated role config group.
  @param cluster_name: Cluster name.
  @return: The updated ApiRoleConfigGroup object.
  """
  body = json.dumps(apigroup.to_json_dict())
  resp = resource_root.put(_get_role_config_group_path(
      cluster_name, service_name, name), data=body)
  return ApiRoleConfigGroup.from_json_dict(resp, resource_root)

def delete_role_config_group(resource_root, service_name, name,
    cluster_name="default"):
  """
  Delete a role config group by name.
  @param resource_root: The root Resource object.
  @param service_name: Service name.
  @param name: Role config group name.
  @param cluster_name: Cluster name.
  @return: The deleted ApiRoleConfigGroup object.
  """
  resp = resource_root.delete(_get_role_config_group_path(
     cluster_name, service_name, name))
  return ApiRoleConfigGroup.from_json_dict(resp, resource_root)

def move_roles(resource_root, service_name, name, role_names,
    cluster_name="default"):
  """
  Moves roles to the specified role config group.
  
  The roles can be moved from any role config group belonging
  to the same service. The role type of the destination group
  must match the role type of the roles.
  
  @param name: The name of the group the roles will be moved to.
  @param role_names: The names of the roles to move.
  @return List of roles which have been moved successfully.
  """    
  path = _get_role_config_group_path(
      cluster_name, service_name, name) + '/roles'
  resp = resource_root.put(path,
      data=json.dumps({ApiList.LIST_KEY : role_names}))
  return ApiList.from_json_dict(ApiRole, resp, resource_root)

def move_roles_to_base_role_config_group(resource_root, service_name,
     role_names, cluster_name="default"):
  """
  Moves roles to the base role config group.
    
  The roles can be moved from any role config group belonging to the same
  service. The role type of the roles may vary. Each role will be moved to
  its corresponding base group depending on its role type.
  
  @param role_names The names of the roles to move.
  @return List of roles which have been moved successfully.
  """
  path = _get_role_config_groups_path(cluster_name, service_name) + '/roles'
  resp = resource_root.put(path,
      data=json.dumps({ApiList.LIST_KEY : role_names}))
  return ApiList.from_json_dict(ApiRole, resp, resource_root)


class ApiRoleConfigGroup(BaseApiObject):
  RO_ATTR = ('base', 'serviceRef')
  """
  name is RW only temporarily; once all RCG names are unique,
  this property will be auto-generated and Read-only
  """
  RW_ATTR = ('name', 'displayName', 'roleType', 'config')

  def __init__(self, resource_root, name, displayName, roleType, config = None):
    BaseApiObject.ctor_helper(**locals())

  def __str__(self):
    return "<ApiRoleConfigGroup>: %s (cluster: %s; service: %s)" % (
        self.name, self.serviceRef.clusterName, self.serviceRef.serviceName)

  def _path(self):
    return _get_role_config_group_path(self.serviceRef.clusterName,
                          self.serviceRef.serviceName,
                          self.name)

  def get_config(self, view = None):
    """
    Retrieve the group's configuration.

    The 'summary' view contains strings as the dictionary values. The full
    view contains ApiConfig instances as the values.

    @param view: View to materialize ('full' or 'summary').
    @return Dictionary with configuration data.
    """
    path = self._path() + '/config'
    resp = self._get_resource_root().get(path,
        params = view and dict(view=view) or None)
    return json_to_config(resp, view == 'full')

  def update_config(self, config):
    """
    Update the group's configuration.

    @param config Dictionary with configuration to update.
    @return Dictionary with updated configuration.
    """
    path = self._path() + '/config'
    resp = self._get_resource_root().put(path, data = config_to_json(config))
    return json_to_config(resp)

  def get_all_roles(self):
    """
    Retrieve the roles in this role config group.
    
    @return List of roles in this role config group.
    """
    path = self._path() + '/roles'
    resp = self._get_resource_root().get(path)
    return ApiList.from_json_dict(ApiRole, resp, self._get_resource_root())

  def move_roles(self, roles):
    """
    Moves roles to this role config group.
    
    The roles can be moved from any role config group belonging
    to the same service. The role type of the destination group
    must match the role type of the roles.
    
    @param roles: The names of the roles to move.
    @return List of roles which have been moved successfully.
    """
    return move_roles(self._get_resource_root(), self.serviceRef.serviceName,
        self.name, roles, self.serviceRef.clusterName)