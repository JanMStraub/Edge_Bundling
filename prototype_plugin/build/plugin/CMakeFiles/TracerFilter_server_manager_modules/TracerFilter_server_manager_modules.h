#ifndef TracerFilter_server_manager_modules_h
#define TracerFilter_server_manager_modules_h

#include "TracerFilter_server_manager_modules_data.h"
#include <string>
#include <vector>

void TracerFilter_server_manager_modules_initialize(std::vector<std::string>& xmls)
{
  (void)xmls;
  {
    char *init_string = TracerFilter_server_manager_modulesMyTracerFilterGetInterfaces();
    xmls.emplace_back(init_string);
    delete [] init_string;
  }
}

#endif
