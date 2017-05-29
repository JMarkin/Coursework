#include "Matrix.h"

using namespace std;


void Matrix::swapStrOnNull(int index, int q) {
    int str = index;
    for (int j = index + 1; j < n; j++)
        if (a[j][q] != 0) {
            str = j;
            break;
        }
    for (int j = 0; j < n; j++)
        swap(a[index][j], a[str][j]);
    swap(b[index], b[str]);
}

Matrix::Matrix(int N,boost::python::list A,boost::python::list B,double e,int nt):n(N),numThread(nt),eps(e) {
    a.resize(N);
    b.resize(N);
    x.resize(N);
    for(int  i=0;i<N;i++)
	a[i].resize(N);
    for(int i=0;i<len(A);i++)
	for(int j=0;j<len(A[i]);j++)
	    a[i][j]=boost::python::extract<double>(A[i][j]);
    for(int j=0;j<len(B);j++)
        b[j]=boost::python::extract<double>(B[j]);
}

boost::python::tuple Matrix::getEquation() {
    boost::python::list a1,b1;
    for(auto q:a){
        boost::python::list p;
        for(auto w:q)
	   p.append(w);
        a1.append(p);
    }
    for(auto q:b)
        b1.append(q);
    return boost::python::make_tuple(a1,b1);
}

void Matrix::straightGaus(){
    int q = 0;
    for (int i = 0; i < n; i++) {
        if (a[i][0] == 0) {
            swapStrOnNull(i, q);
        }
        for (int j = i + 1; j < n; j++) {
            if (a[j][q] == 0)
                continue;
            double k = a[i][q] / a[j][q];
            for (int w = 0; w < n; w++) {
                a[j][w] = a[j][w] * k - a[i][w];
            }
            b[j] = k * b[j] - b[i];
        }
        q++;
    }
}

void Matrix::methodGaus() {
    straightGaus();
    x[n - 1] = b[n - 1] / a[n - 1][n - 1];
    for (int i = n - 2; i >= 0; i--) {
        double s = 0;
        int j;
        for (j = n - 1; j > i; j--) {
            s += a[i][j] * x[j];
        }
        x[i] = (b[i] - s) / a[i][j];
    }
}

boost::python::list Matrix::getAnswer() {
    
    boost::python::list ans;
    for(auto q:x)
	ans.append(q);
    return ans;
}

void Matrix::methodJacobi() {
    double *tempX = new double[n];
    double norm;
    do {
        for (int i = 0; i < n; i++) {
            tempX[i] = b[i];
            for (int g = 0; g < n; g++) {
                if (i != g)
                    tempX[i] -= a[i][g] * x[g];
            }
            tempX[i] /= a[i][i];
        }
        norm = fabs(x[0] - tempX[0]);
        //cout<<norm<<"   ";
        for (int h = 0; h < n; h++) {
            if (fabs(x[h] - tempX[h]) > norm)
                norm = fabs(x[h] - tempX[h]);
            x[h] = tempX[h];
        }
        /*for (auto i : x)
            cout << i << " ";
        cout << endl;*/
    } while (norm > eps);
    delete[] tempX;
}

void Matrix::methodJacobiPrallel() {
    omp_set_num_threads(numThread);
    double **f, **alf, *bet, *x1, max;
    int i, j;
    f = new double *[n];
    for (i = 0; i < n; i++)
        f[i] = new double[n];
    alf = new double *[n];
    for (i = 0; i < n; i++)
        alf[i] = new double[n];
    bet = new double[n];
    x1 = new double[n];
#pragma omp parallel for private (i) schedule(auto)
    for (i = 0; i < n; i++) {
#pragma omp parallel for private (j) schedule(auto)
        for (j = 0; j < n; j++)
            if (i == j) alf[i][j] = 0; else alf[i][j] = -a[i][j] / a[i][i];
        bet[i] = b[i] / a[i][i];
    }
    for (i = 0; i < n; i++)
        x1[i] = bet[i];
    max = 5 * eps;
    while (max > eps) {

        for (i = 0; i < n; i++)
            x[i] = x1[i];
        max = from_methodJacobiPrallel(alf, x1, bet);
    }
}

double Matrix::from_methodJacobiPrallel(double **alf, double *x1, double *bet) {
    int i, j;
    double s, max;
#pragma omp parallel for shared(alf, bet, x, x1) private (i, j, s) schedule(auto)
    for (i = 0; i < n; i++) {
        s = 0;
        for (j = 0; j < n; j++)
            s += alf[i][j] * x[j];
        s += bet[i];
        if (i == 0) max = fabs(x[i] - s);
        else if (fabs(x[i] - s) > max) max = fabs(x[i] - s);
        x1[i] = s;
    }
    return max;
}