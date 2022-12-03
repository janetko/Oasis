//
//  LoginViewController.swift
//  Oasis
//
//  Created by Nick Brenner on 12/1/22.
//

import UIKit

class LoginViewController: UIViewController {
    
    var bear = UIImageView()
    var setupAccountLabel = UILabel()
    var emailTextField = UITextField()
    var passwordTextField = UITextField()
    var loginButton = UIButton()
    var noUser = UILabel()
    var userData: [User] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        
        bear.image = UIImage(named: "BearHat")
        bear.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(bear)
        
        setupAccountLabel.text = "Let's get your account setup!"
        setupAccountLabel.textColor = .red
        setupAccountLabel.font = .systemFont(ofSize: 20)
        setupAccountLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(setupAccountLabel)
        
        emailTextField.placeholder = "Enter your email...                 "
        emailTextField.font = .systemFont(ofSize: 20)
        emailTextField.translatesAutoresizingMaskIntoConstraints = false
        emailTextField.backgroundColor = .white
        view.addSubview(emailTextField)
        
        passwordTextField.placeholder = "Enter your password...           "
        passwordTextField.font = .systemFont(ofSize: 20)
        passwordTextField.translatesAutoresizingMaskIntoConstraints = false
        passwordTextField.backgroundColor = .white
        view.addSubview(passwordTextField)
        
        loginButton.setTitle("Login", for: .normal)
        loginButton.setTitleColor(.white, for: .normal)
        loginButton.layer.backgroundColor = UIColor.red.cgColor
        loginButton.layer.borderWidth = 1
        loginButton.layer.borderColor = UIColor.systemRed.cgColor
        loginButton.layer.cornerRadius = 5
        loginButton.addTarget(self, action: #selector(didSelectLogin), for: .touchUpInside)
        loginButton.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(loginButton)
        
        noUser.text = "Incorrect Login Info"
        noUser.isHidden = true
        noUser.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(noUser)
        
        setupConstraints()
    }
    
    func setupConstraints() {
        NSLayoutConstraint.activate([
            bear.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant:10),
            bear.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        NSLayoutConstraint.activate([
            setupAccountLabel.topAnchor.constraint(equalTo: bear.bottomAnchor, constant: 10),
            setupAccountLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        NSLayoutConstraint.activate([
            emailTextField.topAnchor.constraint(equalTo: setupAccountLabel.bottomAnchor, constant: 70),
            emailTextField.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        NSLayoutConstraint.activate([
            noUser.topAnchor.constraint(equalTo: emailTextField.bottomAnchor, constant: 10),
            noUser.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        NSLayoutConstraint.activate([
            passwordTextField.topAnchor.constraint(equalTo: noUser.bottomAnchor, constant: 20),
            passwordTextField.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        
        NSLayoutConstraint.activate([
            loginButton.topAnchor.constraint(equalTo: passwordTextField.bottomAnchor, constant: 20),
            loginButton.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
    }
    
    @objc func didSelectLogin() {
        
        var found: Bool = false
        
        NetworkManager.login(userEmail: emailTextField.text!, userPassword: passwordTextField.text!) { response in
            if (response != nil) {
                found = true
            }
            if (!found) {
                self.noUser.isHidden = false
                return
            }
            
            self.present(MoodTrackerViewController(), animated: false)
        }
    }
    
}
