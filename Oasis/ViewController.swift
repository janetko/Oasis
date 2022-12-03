//
//  ViewController.swift
//  Oasis
//
//  Created by Krystal Ohuabunwa on 11/26/22.
//

import UIKit


class ViewController: UIViewController {
    var bear = UIImageView()
    var titleLabel = UILabel()
    var purposeLabel = UITextView()
    var createAccountButton = UIButton()
    var loginButton = UIButton()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        
        titleLabel.text = "Oasis"
        titleLabel.textColor = .systemCyan
        titleLabel.font = .systemFont(ofSize: 50)
        titleLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(titleLabel)
        
        bear.image = UIImage(named: "BearHat")
        bear.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(bear)
        
        purposeLabel.text = "An app for Cornell students to stay in touch with friends, create connections with others, and most importantly take care of themselves by checking in daily."
        purposeLabel.isUserInteractionEnabled = false
        purposeLabel.textColor = .systemCyan
        purposeLabel.font = .systemFont(ofSize: 20)
        purposeLabel.textAlignment = .left
        purposeLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(purposeLabel)
        
        createAccountButton.setTitle("Create Account", for: .normal)
        createAccountButton.setTitleColor(.white, for: .normal)
        createAccountButton.layer.backgroundColor = UIColor.red.cgColor
        createAccountButton.layer.borderWidth = 1
        createAccountButton.layer.borderColor = UIColor.systemRed.cgColor
        createAccountButton.layer.cornerRadius = 5
        createAccountButton.addTarget(self, action: #selector(didSelectCreateAccount), for: .touchUpInside)
        createAccountButton.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(createAccountButton)
        
        loginButton.setTitle("I already have an account", for: .normal)
        loginButton.setTitleColor(.red, for: .normal)
        loginButton.addTarget(self, action: #selector(didSelectLogin), for: .touchUpInside)
        loginButton.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(loginButton)
        
        setupConstraints()
    }
    
    func setupConstraints() {
        NSLayoutConstraint.activate([
            titleLabel.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant:10),
            titleLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        NSLayoutConstraint.activate([
            bear.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            bear.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 20),
            bear.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.7),
            bear.heightAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.7)
        ])
        NSLayoutConstraint.activate([
            purposeLabel.topAnchor.constraint(equalTo: bear.bottomAnchor, constant: 20),
            purposeLabel.bottomAnchor.constraint(equalTo: createAccountButton.topAnchor, constant: -20),
            purposeLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            purposeLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20)
        ])
        NSLayoutConstraint.activate([
            createAccountButton.bottomAnchor.constraint(equalTo: loginButton.topAnchor, constant: -20),
            createAccountButton.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        NSLayoutConstraint.activate([
            loginButton.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -10),
            loginButton.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
    }

    
    @objc func didSelectCreateAccount() {
        navigationController?.pushViewController(CreateAccountViewController(delegate: self), animated: true)
    }
    
    @objc func didSelectLogin() {
        navigationController?.pushViewController(LoginViewController(), animated: true)
    }
}

extension ViewController: CreateAccountDelegate {
    func createAccount(name: String, email: String, password: String) {
        NetworkManager.createUser(userName: name, userEmail: email, userPassword: password) { post in
        }
    }
}

    
