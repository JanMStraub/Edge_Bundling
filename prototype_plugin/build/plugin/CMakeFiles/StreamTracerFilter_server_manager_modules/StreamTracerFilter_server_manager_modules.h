#ifndef StreamTracerFilter_server_manager_modules_h
#define StreamTracerFilter_server_manager_modules_h

#include "StreamTracerFilter_server_manager_modules_data.h"
#include <string>
#include <vector>

void StreamTracerFilter_server_manager_modules_initialize(std::vector<std::string>& xmls)
{
  (void)xmls;
  {
    char *init_string = StreamTracerFilter_server_manager_modulesMyStreamTracerFilterGetInterfaces();
    xmls.emplace_back(init_string);
    delete [] init_string;
  }
}

#endif
