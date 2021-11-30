#ifndef ElevationFilter_server_manager_modules_h
#define ElevationFilter_server_manager_modules_h

#include "ElevationFilter_server_manager_modules_data.h"
#include <string>
#include <vector>

void ElevationFilter_server_manager_modules_initialize(std::vector<std::string>& xmls)
{
  (void)xmls;
  {
    char *init_string = ElevationFilter_server_manager_modulesMyElevationFilterGetInterfaces();
    xmls.emplace_back(init_string);
    delete [] init_string;
  }
}

#endif
