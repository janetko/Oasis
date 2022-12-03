//
//  MemoDetailViewController.swift
//  Oasis
//
//  Created by Nick Brenner on 12/2/22.
//

import UIKit

class DetailViewController: UIViewController {
    
    let memoImageView = UIImageView()
    let memoText = UITextField()
    let submitButton = UIButton()

    weak var delegate: ChangeMemoDelegate?

    init(delegate: ChangeMemoDelegate) {
        self.delegate = delegate
        super.init(nibName: nil, bundle: nil)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white

        memoImageView.image = UIImage(named: "BearHat")
        memoImageView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(memoImageView)

        memoText.text = "Tell me how you are doing..."
        memoText.textColor = .black
        memoText.font = .systemFont(ofSize: 20)
        memoText.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(memoText)
        
        submitButton.setTitle("Submit", for: .normal)
        submitButton.setTitleColor(.systemBlue, for: .normal)
        submitButton.addTarget(self, action: #selector(changeContactCell), for: .touchUpInside)
        submitButton.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(submitButton)
        
        setupConstraints()
    }

    @objc func changeContactCell() {
        delegate?.changeMemoText(text: memoText.text!)
        dismiss(animated: true)
    }

    func setupConstraints() {
        NSLayoutConstraint.activate([
            memoImageView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            memoImageView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 20),
            memoImageView.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.5),
            memoImageView.heightAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.5)
        ])

        NSLayoutConstraint.activate([
            memoText.topAnchor.constraint(equalTo: memoImageView.bottomAnchor, constant: 10),
            memoText.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            memoText.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.80),
        ])

        NSLayoutConstraint.activate([
            submitButton.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -30),
            submitButton.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}

protocol ChangeMemoDelegate: UITableViewCell {
    func changeMemoText(text: String)
}
