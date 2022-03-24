// Loadable modules
//
// Generated by /Applications/ParaView/bin/vtkProcessXML-pv5.10
//
#ifndef LagrangianIntegrationModel_server_manager_modules_data_h
#define LagrangianIntegrationModel_server_manager_modules_data_h

#include <cstring>
#include <cassert>
#include <algorithm>


// From file /Users/jan/Google Drive/Programmieren/bachelor_thesis/example_plugin/plugin/LagrangianExample/LagrangianIntegrationModel.xml
static const char* const LagrangianIntegrationModel_server_manager_modulesLagrangianIntegrationModelInterface0 =
"<ServerManagerConfiguration>\n"
"  <ProxyGroup name=\"lagrangian_integration_models\">\n"
"    <Proxy base_proxygroup=\"lagrangian_integration_models_abstract\"\n"
"           base_proxyname=\"BasicIntegrationModel\"\n"
"           class=\"vtkLagrangianIntegrationModelExample\"\n"
"           name=\"LagrangianIntegrationModelExample\"\n"
"           label=\"Integration Model Example\">\n"
"      <StringVectorProperty animateable=\"0\"\n"
"                            command=\"SetInputArrayToProcess\"\n"
"                            default_values_delimiter=\";\"\n"
"                            default_values=\"3;0;0;3;FlowVelocity\"\n"
"                            element_types=\"0 0 0 0 2\"\n"
"                            label=\"Flow Velocity\"\n"
"                            name=\"FlowVelocity\"\n"
"                            number_of_elements=\"5\">\n"
"        <ArrayListDomain name=\"array_list\"\n"
"                         attribute_type=\"Vectors\"\n"
"                         input_domain_name=\"input_array_3\">\n"
"          <RequiredProperties>\n"
"            <Property function=\"Input\"\n"
"                      name=\"DummyInput\" />\n"
"          </RequiredProperties>\n"
"        </ArrayListDomain>\n"
"        <Documentation>This property contains the name of\n"
"        the array to use as flow velocity.</Documentation>\n"
"      </StringVectorProperty>\n"
"      <StringVectorProperty animateable=\"0\"\n"
"                            command=\"SetInputArrayToProcess\"\n"
"                            default_values_delimiter=\";\"\n"
"                            default_values=\"4;0;0;3;FlowDensity\"\n"
"                            element_types=\"0 0 0 0 2\"\n"
"                            label=\"Flow Density\"\n"
"                            name=\"FlowDensity\"\n"
"                            number_of_elements=\"5\">\n"
"        <ArrayListDomain name=\"array_list\"\n"
"                         attribute_type=\"Scalars\"\n"
"                         input_domain_name=\"input_array_1\">\n"
"          <RequiredProperties>\n"
"            <Property function=\"Input\"\n"
"                      name=\"DummyInput\" />\n"
"          </RequiredProperties>\n"
"        </ArrayListDomain>\n"
"        <Documentation>This property contains the name of\n"
"        the array to use as flow density.</Documentation>\n"
"      </StringVectorProperty>\n"
"      <StringVectorProperty animateable=\"0\"\n"
"                            command=\"SetInputArrayToProcess\"\n"
"                            default_values_delimiter=\";\"\n"
"                            default_values=\"5;0;0;3;FlowDynamicViscosity\"\n"
"                            element_types=\"0 0 0 0 2\"\n"
"                            label=\"Flow Dynamic Viscosity\"\n"
"                            name=\"FlowDynamicViscosity\"\n"
"                            number_of_elements=\"5\">\n"
"        <ArrayListDomain name=\"array_list\"\n"
"                         input_domain_name=\"input_array_1\">\n"
"          <RequiredProperties>\n"
"            <Property function=\"Input\"\n"
"                      name=\"DummyInput\" />\n"
"          </RequiredProperties>\n"
"        </ArrayListDomain>\n"
"        <Documentation>This property contains the name of\n"
"        the array to use as flow dynamic viscosity.</Documentation>\n"
"      </StringVectorProperty>\n"
"      <StringVectorProperty animateable=\"0\"\n"
"                            command=\"SetInputArrayToProcess\"\n"
"                            default_values_delimiter=\";\"\n"
"                            default_values=\"6;1;0;0;ParticleDiameter\"\n"
"                            element_types=\"0 0 0 0 2\"\n"
"                            label=\"ParticleDiameter\"\n"
"                            name=\"Particle Diameter\"\n"
"                            number_of_elements=\"5\">\n"
"        <ArrayListDomain name=\"array_list\"\n"
"                         input_domain_name=\"source_array_point_1\">\n"
"          <RequiredProperties>\n"
"            <Property function=\"Input\"\n"
"                      name=\"DummySource\" />\n"
"          </RequiredProperties>\n"
"        </ArrayListDomain>\n"
"        <Documentation>This property contains the name of\n"
"        the array to use from seeds as particle diameter.</Documentation>\n"
"      </StringVectorProperty>\n"
"      <StringVectorProperty animateable=\"0\"\n"
"                            command=\"SetInputArrayToProcess\"\n"
"                            default_values_delimiter=\";\"\n"
"                            default_values=\"7;1;0;0;ParticleDensity\"\n"
"                            element_types=\"0 0 0 0 2\"\n"
"                            label=\"ParticleDensity\"\n"
"                            name=\"Particle Density\"\n"
"                            number_of_elements=\"5\">\n"
"        <ArrayListDomain name=\"array_list\"\n"
"                         input_domain_name=\"source_array_point_1\">\n"
"          <RequiredProperties>\n"
"            <Property function=\"Input\"\n"
"                      name=\"DummySource\" />\n"
"          </RequiredProperties>\n"
"        </ArrayListDomain>\n"
"        <Documentation>This property contains the name of\n"
"        the array to use from seeds as particle density.</Documentation>\n"
"      </StringVectorProperty>\n"
"      <StringVectorProperty animateable=\"0\"\n"
"                            command=\"SetInputArrayToProcess\"\n"
"                            default_values_delimiter=\";\"\n"
"                            default_values=\"8;0;0;2;GravityConstant\"\n"
"                            element_types=\"0 0 0 0 2\"\n"
"                            label=\"GravityConstant\"\n"
"                            name=\"Gravity Constant\"\n"
"                            number_of_elements=\"5\">\n"
"        <ArrayListDomain name=\"array_list\"\n"
"                         input_domain_name=\"input_array_field\">\n"
"          <RequiredProperties>\n"
"            <Property function=\"Input\"\n"
"                      name=\"DummyInput\" />\n"
"          </RequiredProperties>\n"
"        </ArrayListDomain>\n"
"        <Documentation>This property contains the name of\n"
"        the array to use from flow input as gravity constant.</Documentation>\n"
"      </StringVectorProperty>\n"
"      </Proxy>\n"
"  </ProxyGroup>\n"
"</ServerManagerConfiguration>\n"
"\n";
// Get single string
inline char* LagrangianIntegrationModel_server_manager_modulesLagrangianIntegrationModelGetInterfaces()
{

  const size_t len0 = strlen(LagrangianIntegrationModel_server_manager_modulesLagrangianIntegrationModelInterface0);
  size_t len = ( 0
    + len0 );
  char* res = new char[ len + 1];
  size_t offset = 0;
  std::copy(LagrangianIntegrationModel_server_manager_modulesLagrangianIntegrationModelInterface0, LagrangianIntegrationModel_server_manager_modulesLagrangianIntegrationModelInterface0 + len0, res + offset); offset += len0;
  assert(offset == len);
  res[offset] = 0;
  return res;
}



#endif
