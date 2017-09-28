#!/usr/bin/env groovy

/*** Variables ***/

// Parameters

def branch = params.branch


// For git
def gitCreds = 'derek'
def gitNgxSwag = 'github.com/dejonghe/ngx-swag.git'

node() {
    stage('prep') {
        dir('ngx-swag'){
            echo "Pulling ngx-swag code from branch \"${branch}\""
            git url: gitNgxSwag, credentialsId: gitCreds, branch: "${branch}"
        }
    }
    stage('build_dist') {
        dir('ngx-swag'){
            echo "Building ngx-swag"
            sh "python setup.py sdist"
        }
    }
}
