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
#include <vtkColorTransferFunction.h>


int main () {
    // simply set filename here (oh static joy)
    std::string inputFilename = "/Users/jan/Google Drive/Programmieren/bachelor_thesis/vtkPrototype/data/tmp_3D.vtk";

    // Get all data from the file
    vtkSmartPointer<vtkUnstructuredGridReader> reader = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(inputFilename.c_str());
    reader->Update();
    
    std::cout << "Test" << std::endl;
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

    vtkSmartPointer<vtkVertexGlyphFilter> vertexGlyphFilter = vtkSmartPointer<vtkVertexGlyphFilter>::New();
    vertexGlyphFilter->SetInputData(poly);

    vtkSmartPointer<vtkPolyDataMapper> signedDistanceMapper = vtkSmartPointer<vtkPolyDataMapper>::New();
    signedDistanceMapper->SetInputConnection(vertexGlyphFilter->GetOutputPort() );
    signedDistanceMapper->ScalarVisibilityOn();

    double colors[5][3] = { { 0, 0, 1},
                            { 0, 0.5, 0.5 },
                            { 0, 1, 0 },
                            { 0.5, 0.5, 0 },
                            { 1, 0, 0 } };
    vtkSmartPointer<vtkColorTransferFunction> colorFunction =
            vtkSmartPointer<vtkColorTransferFunction>::New();
    colorFunction->SetUseBelowRangeColor( true );
    colorFunction->SetBelowRangeColor( colors[0] );
    colorFunction->SetNanColor( colors[0] );
    colorFunction->AddRGBPoint( -0.4, colors[0][0], colors[0][1], colors[0][2] );
    colorFunction->AddRGBPoint( 0, colors[1][0], colors[1][1], colors[1][2] );
    colorFunction->AddRGBPoint( 0.6, colors[2][0], colors[2][1], colors[2][2] );
    colorFunction->AddRGBPoint( 1.5, colors[3][0], colors[3][1], colors[3][2] );
    colorFunction->AddRGBPoint( 2.9, colors[4][0], colors[4][1], colors[4][2] );
    colorFunction->Build();

    signedDistanceMapper->SetLookupTable(colorFunction);
    signedDistanceMapper->UseLookupTableScalarRangeOn();

    vtkSmartPointer<vtkActor> signedDistanceActor = vtkSmartPointer<vtkActor>::New();
    signedDistanceActor->SetMapper(signedDistanceMapper);

    vtkSmartPointer<vtkRenderer> renderer = vtkSmartPointer<vtkRenderer>::New();
    renderer->AddViewProp(signedDistanceActor);

    vtkSmartPointer<vtkRenderWindow> renderWindow = vtkSmartPointer<vtkRenderWindow>::New();
    renderWindow->AddRenderer(renderer);

    vtkSmartPointer<vtkRenderWindowInteractor> renWinInteractor = vtkSmartPointer<vtkRenderWindowInteractor>::New();
    renWinInteractor->SetRenderWindow(renderWindow);

    renderWindow->Render();
    renWinInteractor->Start();

    return EXIT_SUCCESS;
}