//
//  NetworkManager.swift
//  Oasis
//
//  Created by Nick Brenner on 11/29/22.
//

import UIKit
import Alamofire
import Foundation

class NetworkManager {
    static let host = "http://34.86.118.159"
    
    static func getAllUsers(completion: @escaping ([User]) -> Void) {
        let endpoint = "\(host)/users/"
        AF.request(endpoint, method: .get).validate().responseData { response in
            switch response.result {
            case .success(let data):
                let jsonDecoder = JSONDecoder()
                if let userResponse = try? jsonDecoder.decode(UserResponse.self, from: data) {
                    completion(userResponse.users)
                } else {
                    print("Failed to decode")
                }
            case .failure(let error):
                print(error.localizedDescription)
            }
        }
    }
    
    static func createUser(userName: String, userEmail: String, userPassword: String, completion: @escaping (SessionToken) -> Void) {
        let endpoint = "\(host)/users/register/"
        
        let params: Parameters = [
            "name": userName,
            "username": userEmail,
            "password": userPassword
        ]
        AF.request(endpoint, method: .post, parameters: params, encoding: JSONEncoding.default).validate().responseData { response in
            switch response.result {
            case .success(let data):
                let jsonDecoder = JSONDecoder()
                if let userResponse = try? jsonDecoder.decode(SessionToken.self, from: data) {
                    completion(userResponse)
                } else {
                    print("Failed to decode createPost")
                }
            
            case .failure(let error):
                print(error.localizedDescription)
            }
        }
    }
    
    static func login(userEmail: String, userPassword: String, completion: @escaping (SessionToken?) -> Void) {
        let endpoint = "\(host)/users/login/"
        
        let params: Parameters = [
            "username": userEmail,
            "password": userPassword
        ]
        AF.request(endpoint, method: .post, parameters: params, encoding: JSONEncoding.default).validate().responseData { response in
            switch response.result {
            case .success(let data):
                let jsonDecoder = JSONDecoder()
                if let userResponse = try? jsonDecoder.decode(SessionToken.self, from: data) {
                    completion(userResponse)
                } else {
                    print("Failed to decode createPost")
                }
            
            case .failure(let error):
                print(error.localizedDescription)
                completion(nil)
            }
        }
    }
    
}
