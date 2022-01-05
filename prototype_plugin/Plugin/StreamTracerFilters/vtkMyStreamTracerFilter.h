#ifndef vtkMyStreamTracer_h
#define vtkMyStreamTracer_h

#include "StreamTracerFiltersModule.h"

class vtkMyStreamTracerFilter {
  public:
    void calculateVelocity();

  protected:
    vtkMyStreamTracerFilter(){};
    ~vtkMyStreamTracerFilter(){};
};

#endif //vtkMyStreamTracer_h