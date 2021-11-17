#include <string>
#include <iostream>

#include <vtkSmartPointer.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkUnstructuredGrid.h>
#include <vtkFloatArray.h>
#include <vtkNew.h>
#include <vtkPolyData.h>
#include <vtkPointData.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>
#include <vtkScalarBarActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkVertexGlyphFilter.h>

int main () {

    std::cout << "Program start" << std::endl;

    std::string inputFilename = "/Users/jan/Google Drive/Programmieren/bachelor_thesis/vtkPrototype/data/tmp_3D.vtk";

    vtkNew<vtkUnstructuredGridReader> reader;
    reader->SetFileName(inputFilename.c_str());
    reader->Update();

    vtkUnstructuredGrid* output = reader->GetOutput();

    int numberOfPoints = output->GetNumberOfPoints();
    vtkNew<vtkFloatArray> scalars;
    scalars->SetNumberOfValues(numberOfPoints);

    for (int i = 0; i < numberOfPoints; ++i) {
        scalars->SetValue(i, static_cast<float>(i) / numberOfPoints);
    }
    
    vtkNew<vtkPolyData> poly;
    poly->DeepCopy(output);
    poly->GetPointData()->SetScalars(scalars);

    vtkNew<vtkVertexGlyphFilter> vertexGlyphFilter;
    vertexGlyphFilter->SetInputData(poly);

    vtkNew<vtkPolyDataMapper> signedDistanceMapper;
    signedDistanceMapper->SetInputConnection(vertexGlyphFilter->GetOutputPort() );
    signedDistanceMapper->ScalarVisibilityOn();

    vtkNew<vtkActor> signedDistanceActor;
    signedDistanceActor->SetMapper(signedDistanceMapper);

    vtkNew<vtkRenderer> renderer;
    renderer->AddViewProp(signedDistanceActor);

    vtkNew<vtkRenderWindow> renderWindow;
    renderWindow->AddRenderer(renderer);

    vtkNew<vtkRenderWindowInteractor> renWinInteractor;
    renWinInteractor->SetRenderWindow(renderWindow);

    renderWindow->Render();
    renWinInteractor->Start();

    return EXIT_SUCCESS;
}