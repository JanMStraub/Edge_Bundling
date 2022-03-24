#ifndef LagrangianIntegrationModel_server_manager_modules_h
#define LagrangianIntegrationModel_server_manager_modules_h

#include "LagrangianIntegrationModel_server_manager_modules_data.h"
#include <string>
#include <vector>

void LagrangianIntegrationModel_server_manager_modules_initialize(std::vector<std::string>& xmls)
{
  (void)xmls;
  {
    char *init_string = LagrangianIntegrationModel_server_manager_modulesLagrangianIntegrationModelGetInterfaces();
    xmls.emplace_back(init_string);
    delete [] init_string;
  }
}

#endif
