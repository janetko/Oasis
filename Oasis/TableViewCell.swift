//
//  TableViewCell.swift
//  Oasis
//
//  Created by Nick Brenner on 12/2/22.
//

import UIKit

class TableViewCell: UITableViewCell {

    let memoImageView = UIImageView()
    let memoText = UITextField()

    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        
        memoImageView.image = UIImage(named: "BearHat")
        memoImageView.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(memoImageView)
        
        memoText.isUserInteractionEnabled = false
        memoText.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(memoText)
        
        setupConstraints()
    }
    
    func setupConstraints() {
        NSLayoutConstraint.activate([
            memoImageView.leadingAnchor.constraint(equalTo: contentView.leadingAnchor),
            memoImageView.heightAnchor.constraint(equalTo: contentView.widthAnchor, multiplier: 0.33),
            memoImageView.widthAnchor.constraint(equalTo: contentView.widthAnchor, multiplier: 0.33),
            memoImageView.topAnchor.constraint(equalTo: contentView.topAnchor),
            memoImageView.bottomAnchor.constraint(equalTo: contentView.bottomAnchor)
        ])
        
        NSLayoutConstraint.activate([
            memoText.leadingAnchor.constraint(equalTo: memoImageView.trailingAnchor, constant: 10),
            memoText.topAnchor.constraint(equalTo: contentView.topAnchor),
            memoText.centerXAnchor.constraint(equalTo: contentView.centerXAnchor)
        ])
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        // Configure the view for the selected state
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
}

extension TableViewCell: ChangeMemoDelegate {
    func changeMemoText(text: String) {
        memoText.text = text
    }
}
