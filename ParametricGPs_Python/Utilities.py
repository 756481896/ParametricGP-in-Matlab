#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import autograd.numpy as np

def kernel(a, b, hyp):
    output_scale = np.exp(hyp[0])
    lengthscales = np.sqrt(np.exp(hyp[1:]))
    a = a/lengthscales
    b = b/lengthscales
    aSumSquare = np.sum(np.square(a),axis=1);
    bSumSquare = np.sum(np.square(b),axis=1);
    mul = np.dot(a,b.T);
    dists = aSumSquare[:,np.newaxis]+bSumSquare-2.0*mul
    return output_scale * np.exp(-0.5 * dists)

def stochastic_update_Adam(w,grad_w,mt,vt,lrate,iteration):
    beta1 = 0.9;
    beta2 = 0.999;
    epsilon = 1e-8;

    mt = mt*beta1 + (1.0-beta1)*grad_w;
    vt = vt*beta2 + (1.0-beta2)*grad_w**2;

    mt_hat = mt/(1.0-beta1**iteration);
    vt_hat = vt/(1.0-beta2**iteration);

    scal = 1.0/(np.sqrt(vt_hat) + epsilon);

    w = w - lrate*mt_hat*scal;
    
    return w,mt,vt

def Normalize(X, X_m, X_s):
    return (X-X_m)/(X_s)
     
def Denormalize(X, X_m, X_s):    
    return X_s*X + X_m

def fetch_minibatch(X,y,N_batch):
    N = X.shape[0]
    idx = np.random.permutation(N)
    X_batch = X[idx[0:N_batch],:]
    y_batch = y[idx[0:N_batch]]
    return X_batch, y_batch