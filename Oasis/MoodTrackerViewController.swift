//
//  MoodTrackerViewController.swift
//  Oasis
//
//  Created by Nick Brenner on 12/2/22.
//

import UIKit

class MoodTrackerViewController: UIViewController {

    let header = UILabel()
    let memoTableView = UITableView()
    let reuseIdentifier = "contactReuseIdentifier"
    
    override func viewDidLoad() {
        super.viewDidLoad()

        view.backgroundColor = .white
        
        header.text = "My Memos"
        header.textColor = .black
        header.font = .systemFont(ofSize: 20, weight: .bold)
        
        header.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(header)
    
        memoTableView.translatesAutoresizingMaskIntoConstraints = false
        memoTableView.dataSource = self
        memoTableView.delegate = self
        memoTableView.register(TableViewCell.self, forCellReuseIdentifier: reuseIdentifier)
        view.addSubview(memoTableView)
        
        setupConstraints()
    }

    func setupConstraints() {

        NSLayoutConstraint.activate([
            header.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor,
                                           constant: 20),
            header.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])

        NSLayoutConstraint.activate([
            memoTableView.topAnchor.constraint(equalTo: header.bottomAnchor, constant: 20),
            memoTableView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor),
            memoTableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            memoTableView.trailingAnchor.constraint(equalTo: view.trailingAnchor)
        ])
    }
}
extension MoodTrackerViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 10
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        if let cell = memoTableView.dequeueReusableCell(withIdentifier: reuseIdentifier, for: indexPath) as? TableViewCell {
            return cell
        }
        else {
            return UITableViewCell()
        }
    }
}
extension MoodTrackerViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let cell = memoTableView.cellForRow(at: indexPath) as! TableViewCell
        present(DetailViewController(delegate: cell), animated: true)
    }
}
