#include "Matrix.h"
#include <boost/python.hpp>


BOOST_PYTHON_MODULE( Matrix )
{
    using namespace boost::python;
    class_<Matrix>("Matrix",init<int,boost::python::list,boost::python::list,double,int>())

            .def("getEquation",&Matrix::getEquation)
            .def("methodGaus",&Matrix::methodGaus)
            .def("methodJacobi",&Matrix::methodJacobi)
            .def("getAnswer",&Matrix::getAnswer)
            .def("methodJacobiPrallel",&Matrix::methodJacobiPrallel)
                    ;
}
