#ifndef vtkMyTracerFilter_h
#define vtkMyTracerFilter_h

#include <vector>

#include "vtkPolyDataAlgorithm.h"
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

class vtkMyTracerFilter : public vtkPolyDataAlgorithm {
  public:
    vtkTypeMacro(vtkMyTracerFilter, vtkPolyDataAlgorithm);

    static vtkMyTracerFilter* New();

    void calculateVelocity();
    void calculateStreamlines();
    void calculatePathlines();

    /**
     * All I/O operations
     */

    // Specify starting point (seed) of streamline
    vtkSetVector3Macro(StartPosition, double);
    vtkGetVector3Macro(StartPosition, double);

    // Specify the source object
    void SetSourceData(vtkDataSet* source);
    vtkDataSet* GetSource();

    // Max length of streamline from LENGTH_UNIT
    vtkSetMacro(MaximumPropagation, double);
    vtkGetMacro(MaximumPropagation, double);

    // Size of uniform integration step 
    void SetIntegrationStepUnit(int unit);
    int GetIntegrationStepUnit() { return this->IntegrationStepUnit; }

    // Initial step size for line integration
    vtkSetMacro(InitialIntegrationStep, double);
    vtkGetMacro(InitialIntegrationStep, double);

    // Minimum step size for line integration
    vtkSetMacro(MinimumIntegrationStep, double);
    vtkGetMacro(MinimumIntegrationStep, double);

    // Maximum step size for line integration
    vtkSetMacro(MaximumIntegrationStep, double);
    vtkGetMacro(MaximumIntegrationStep, double);

    // Maximum error
    vtkSetMacro(MaximumError, double);
    vtkGetMacro(MaximumError, double);

    // Max number of steps
    vtkSetMacro(MaximumNumberOfSteps, vtkIdType);
    vtkGetMacro(MaximumNumberOfSteps, vtkIdType);
    
    // Terminal speed value
    vtkSetMacro(TerminalSpeed, double);
    vtkGetMacro(TerminalSpeed, double);

    // Compute streamlines on surface?
    vtkGetMacro(SurfaceStreamlines, bool);
    vtkSetMacro(SurfaceStreamlines, bool);
    vtkBooleanMacro(SurfaceStreamlines, bool);

    void SetIntegrator(vtkInitialValueProblemSolver*);
    vtkGetObjectMacro(Integrator, vtkInitialValueProblemSolver);
    void SetIntegratorType(int type);
    int GetIntegratorType();
    void SetIntegratorTypeToRungeKutta2() { this->SetIntegratorType(RUNGE_KUTTA2); }
    void SetIntegratorTypeToRungeKutta4() { this->SetIntegratorType(RUNGE_KUTTA4); }
    void SetIntegratorTypeToRungeKutta45() { this->SetIntegratorType(RUNGE_KUTTA45); }

    void SetInterpolatorTypeToDataSetPointLocator();

    void SetInterpolatorTypeToCellLocator();

    // Integrate up- or downstream
    vtkSetClampMacro(IntegrationDirection, int, FORWARD, BOTH);
    vtkGetMacro(IntegrationDirection, int);
    void SetIntegrationDirectionToForward() { this->SetIntegrationDirection(FORWARD); }
    void SetIntegrationDirectionToBackward() { this->SetIntegrationDirection(BACKWARD); }
    void SetIntegrationDirectionToBoth() { this->SetIntegrationDirection(BOTH); }

    // Vorticity on/off
    vtkSetMacro(ComputeVorticity, bool);
    vtkGetMacro(ComputeVorticity, bool);

    // Object for Interpolation
    void SetInterpolatorPrototype(vtkAbstractInterpolatedVelocityField* ivf);
    void SetInterpolatorType(int interpType);

    typedef bool (*CustomTerminationCallbackType)(
        void* clientdata, vtkPoints* points, vtkDataArray* velocity, int integrationDirection);


    /**
     * All enums
     */

    enum Units {
      LENGTH_UNIT = 1,
      CELL_LENGTH_UNIT = 2
    };

    enum Solvers {
      RUNGE_KUTTA2,
      RUNGE_KUTTA4,
      RUNGE_KUTTA45,
      NONE,
      UNKNOWN
    };

    enum ReasonForTermination {
        OUT_OF_DOMAIN = vtkInitialValueProblemSolver::OUT_OF_DOMAIN,
        NOT_INITIALIZED = vtkInitialValueProblemSolver::NOT_INITIALIZED,
        UNEXPECTED_VALUE = vtkInitialValueProblemSolver::UNEXPECTED_VALUE,
        OUT_OF_LENGTH = 4,
        OUT_OF_STEPS = 5,
        STAGNATION = 6,
        FIXED_REASONS_FOR_TERMINATION_COUNT
    };

    enum {
      FORWARD,
      BACKWARD,
      BOTH
    };

    enum {
      INTERPOLATOR_WITH_DATASET_POINT_LOCATOR,
      INTERPOLATOR_WITH_CELL_LOCATOR
    };


    /**
     * Rest
     */

    void AddCustomTerminationCallback(
      CustomTerminationCallbackType callback, void* clientdata, int reasonForTermination);

  protected:
    vtkMyTracerFilter();
    ~vtkMyTracerFilter();

    // Create a default executive.
    vtkExecutive* CreateDefaultExecutive() override;

    // hide the superclass' AddInput() from the user and the compiler
    void AddInput(vtkDataObject*) {
      vtkErrorMacro(<< "AddInput() must be called with a vtkDataSet not a vtkDataObject.");
    }

    int RequestData(vtkInformation*, vtkInformationVector**, vtkInformationVector*) override;
    int FillInputPortInformation(int, vtkInformation*) override;

    void CalculateVorticity(
      vtkGenericCell* cell, double pcoords[3], vtkDoubleArray* cellVectors, double vorticity[3]);
    void Integrate(vtkPointData* inputData, vtkPolyData* output, vtkDataArray* seedSource,
      vtkIdList* seedIds, vtkIntArray* integrationDirections, double lastPoint[3],
      vtkAbstractInterpolatedVelocityField* func, int maxCellSize, int vecType,
      const char* vecFieldName, double& propagation, vtkIdType& numSteps, double& integrationTime);
    double SimpleIntegrate(double seed[3], double lastPoint[3], double stepSize,
      vtkAbstractInterpolatedVelocityField* func);
    int CheckInputs(vtkAbstractInterpolatedVelocityField*& func, int* maxCellSize);
    void GenerateNormals(vtkPolyData* output, double* firstNormal, const char* vecName);

    bool GenerateNormalsInIntegrate;

    // starting from global x-y-z position
    double StartPosition[3];

    static const double EPSILON;
    double TerminalSpeed;

    double LastUsedStepSize;

    struct IntervalInformation {
      double Interval;
      int Unit;
    };

    double MaximumPropagation;
    double MinimumIntegrationStep;
    double MaximumIntegrationStep;
    double InitialIntegrationStep;

    void ConvertIntervals(
      double& step, double& minStep, double& maxStep, int direction, double cellLength);
    static double ConvertToLength(double interval, int unit, double cellLength);
    static double ConvertToLength(IntervalInformation& interval, double cellLength);

    int SetupOutput(vtkInformation* inInfo, vtkInformation* outInfo);
    void InitializeSeeds(vtkDataArray*& seeds, vtkIdList*& seedIds,
      vtkIntArray*& integrationDirections, vtkDataSet* source);

    int IntegrationStepUnit;
    int IntegrationDirection;

    // Prototype showing the integrator type to be set by the user.
    vtkInitialValueProblemSolver* Integrator;

    double MaximumError;
    vtkIdType MaximumNumberOfSteps;

    bool ComputeVorticity;
    double RotationScale;

    // Compute streamlines only on surface.
    bool SurfaceStreamlines;

    vtkAbstractInterpolatedVelocityField* InterpolatorPrototype;

    vtkCompositeDataSet* InputData;
    bool
      HasMatchingPointAttributes; // does the point data in the multiblocks have the same attributes?
    std::vector<CustomTerminationCallbackType> CustomTerminationCallback;
    std::vector<void*> CustomTerminationClientData;
    std::vector<int> CustomReasonForTermination;

    friend class PStreamTracerUtils;

  private:
    vtkMyTracerFilter(const vtkMyTracerFilter&) = delete;
    void operator=(const vtkMyTracerFilter&) = delete;

};

#endif //vtkMyTracerFilter_h