#pragma once
#ifndef EXAMPLE2_LIBRARY_H
#define EXAMPLE2_LIBRARY_H

#include <iostream>
#include <vector>
#include <boost/python.hpp>
#include <omp.h>
using namespace std;

class Matrix {
private:
    vector<vector<double> > a;
    vector<double> b;
    vector<double> x;
    int n;

    void swapStrOnNull(int index, int q);
    double from_methodJacobiPrallel(double **alf, double *x1, double *bet);
    double eps;
    int numThread;
public:

    Matrix(int N,boost::python::list A,boost::python::list B,double e,int nt);

    boost::python::tuple getEquation();

    void methodGaus();

    void straightGaus();

    boost::python::list getAnswer();

    void methodJacobi();
    
    void methodJacobiPrallel();

};

#endif
