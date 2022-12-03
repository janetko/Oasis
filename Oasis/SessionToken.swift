//
//  SessionToken.swift
//  Oasis
//
//  Created by Nick Brenner on 12/2/22.
//

import Foundation

struct SessionToken: Codable {
    let session_token: String
    let session_expiration: String
    let update_token: String
}
