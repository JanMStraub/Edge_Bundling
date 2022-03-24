#ifndef vtkMyTracerFilter_h
#define vtkMyTracerFilter_h

#include <vector>

#include "vtkLagrangianBasicIntegrationModel.h"
#include "vtkInitialValueProblemSolver.h" // Needed for constants

#include "TracerFiltersModule.h"

class vtkAbstractInterpolatedVelocityField;
class vtkCompositeDataSet;
class vtkDataArray;
class vtkDataSetAttributes;
class vtkDoubleArray;
class vtkExecutive;
class vtkGenericCell;
class vtkIdList;
class vtkIntArray;
class vtkPoints;

class vtkMyTracerFilter : public vtkLagrangianBasicIntegrationModel { // before vtkPolyDataAlgorithm
  public:
    vtkTypeMacro(vtkMyTracerFilter, vtkLagrangianBasicIntegrationModel);
    void PrintSelf(ostream& os, vtkIndent indent) override;

    static vtkMyTracerFilter* New();

    using Superclass::FunctionValues;

    vtkGetMacro()

    void calculateVelocity();
    void calculateStreamlines();
    void calculatePathlines();

  protected:
    vtkMyTracerFilter();
    ~vtkMyTracerFilter() override = default;




  private:
    vtkMyTracerFilter(const vtkMyTracerFilter&) = delete;
    void operator=(const vtkMyTracerFilter&) = delete;

};

#endif //vtkMyTracerFilter_h