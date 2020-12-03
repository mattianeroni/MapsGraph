//
// Created by mattia on 02/12/20.
//


#include "Tensor.h"

//
// Constructor for empty Tensor
//
template<typename N>
Tensor<N>::Tensor(int x, int y) : rows(x), cols(y){
    t = new N*[rows];
    for (int i = 0; i < x; ++i){
        t[i] = new N*[cols];
        for (int j = 0; j < y; ++j){
            t[i][j] = 0;
        }
    }
}

//
// Constructor for Tensor using row pointers
//
template<typename N>
Tensor<N>::Tensor(int x, int y, N** content) : rows(x), cols(y){
    t = new N*[rows];
    for (int i = 0; i < x; ++i){
        t[i] = new N*[cols];
        for (int j = 0; j < y; ++j){
            t[i][j] = content[i][j];
        }
    }
}

//
// Constructor for Tensor using vector
//
template<typename N>
Tensor<N>::Tensor(int x, int y, std::vector<std::vector<N>> content) : rows(x), cols(y){
    t = new N*[rows];
    for (int i = 0; i < x; ++i){
        t[i] = new N*[cols];
        for (int j = 0; j < y; ++j){
            t[i][j] = content[i][j];
        }
    }
}


//
// Deconstructor
//
template<typename N>
Tensor<N>::~Tensor () {
    for (int i = 0; i < rows; ++i)
        delete[] t[i];
    delete[] t;
}

//
// Get the size of the Tensor
//
template<typename N>
int* Tensor<N>::size () {
    int s[2] = {rows, cols};
    return s;
}


//
// Get operator for content
//
template<typename N>
N Tensor<N>::operator()(int x, int y){
    return t[x][y];
}
