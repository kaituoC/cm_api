// Licensed to Cloudera, Inc. under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  Cloudera, Inc. licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
package com.cloudera.api.model;

// TODO: get rid of the following annotation when we upgrade to Jackson 1.9.
import org.codehaus.jackson.annotate.JsonProperty;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlRootElement;
import java.util.List;

/**
 * A list of clusters.
 */
@XmlRootElement(name = "clusterList")
public class ApiClusterList extends ApiListBase<ApiCluster> {

  public ApiClusterList() {

  }

  public ApiClusterList(List<ApiCluster> clusters) {
    super(clusters);
  }


  @XmlElementWrapper(name = ApiListBase.ITEMS_ATTR)
  @XmlElement(name = "cluster")
  @JsonProperty(value = ApiListBase.ITEMS_ATTR)
  public List<ApiCluster> getClusters() {
    return values;
  }

}