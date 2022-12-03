//
//  User.swift
//  Oasis
//
//  Created by Nick Brenner on 12/1/22.
//

import Foundation

struct User: Codable {
    let id: Int
    let username: String
    let password: String
}

struct UserResponse: Codable {
    let users: [User]
}
