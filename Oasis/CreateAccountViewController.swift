//
//  CreateAccountViewController.swift
//  Oasis
//
//  Created by Nick Brenner on 12/1/22.
//

import UIKit

class CreateAccountViewController: UIViewController {
    var bear = UIImageView()
    var setupAccountLabel = UILabel()
    var nameTextField = UITextField()
    var emailTextField = UITextField()
    var passwordTextField = UITextField()
    var signUpButton = UIButton()
    
    weak var delegate: CreateAccountDelegate?
    
    init(delegate: CreateAccountDelegate) {
        self.delegate = delegate
        super.init(nibName: nil, bundle: nil)
    }
    
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
        
        nameTextField.placeholder = "Enter your name...              "
        nameTextField.font = .systemFont(ofSize: 20)
        nameTextField.translatesAutoresizingMaskIntoConstraints = false
        nameTextField.backgroundColor = .white
        view.addSubview(nameTextField)
        
        emailTextField.placeholder = "Enter your email...              "
        emailTextField.font = .systemFont(ofSize: 20)
        emailTextField.translatesAutoresizingMaskIntoConstraints = false
        emailTextField.backgroundColor = .white
        view.addSubview(emailTextField)
        
        passwordTextField.placeholder = "Create a password...         "
        passwordTextField.font = .systemFont(ofSize: 20)
        passwordTextField.translatesAutoresizingMaskIntoConstraints = false
        passwordTextField.backgroundColor = .white
        view.addSubview(passwordTextField)
        
        signUpButton.setTitle("Sign Up", for: .normal)
        signUpButton.setTitleColor(.white, for: .normal)
        signUpButton.layer.backgroundColor = UIColor.red.cgColor
        signUpButton.layer.borderWidth = 1
        signUpButton.layer.borderColor = UIColor.systemRed.cgColor
        signUpButton.layer.cornerRadius = 5
        signUpButton.addTarget(self, action: #selector(didSelectSignUp), for: .touchUpInside)
        signUpButton.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(signUpButton)
        
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
            nameTextField.topAnchor.constraint(equalTo: setupAccountLabel.bottomAnchor, constant: 130),
            nameTextField.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        NSLayoutConstraint.activate([
            emailTextField.topAnchor.constraint(equalTo: nameTextField.bottomAnchor, constant: 20),
            emailTextField.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        NSLayoutConstraint.activate([
            passwordTextField.topAnchor.constraint(equalTo: emailTextField.bottomAnchor, constant: 20),
            passwordTextField.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        NSLayoutConstraint.activate([
            signUpButton.topAnchor.constraint(equalTo: passwordTextField.bottomAnchor, constant: 20),
            signUpButton.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
    }
    
    @objc func didSelectSignUp() {
        
        NetworkManager.createUser(userName: nameTextField.text!, userEmail: emailTextField.text!, userPassword: passwordTextField.text!) { response in
        }
        
        present(MoodTrackerViewController(), animated: true)
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}

protocol CreateAccountDelegate: UIViewController {
    func createAccount(name: String, email: String, password: String)
}
