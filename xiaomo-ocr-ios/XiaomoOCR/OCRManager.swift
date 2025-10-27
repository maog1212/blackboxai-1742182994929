//
//  OCRManager.swift
//  OCR 识别管理器
//

import SwiftUI
import UIKit

@MainActor
class OCRManager: ObservableObject {
    @Published var recognizedText: String = ""
    @Published var isProcessing: Bool = false
    @Published var errorMessage: String?

    // 服务器配置
    @AppStorage("serverURL") private var serverURL: String = "http://localhost:5000"
    @AppStorage("useLocalServer") private var useLocalServer: Bool = true

    // 识别图片文字
    func recognizeText(
        from image: UIImage,
        mode: OCRMode,
        resolution: Resolution
    ) async {
        isProcessing = true
        errorMessage = nil
        recognizedText = ""

        do {
            // 压缩图片
            guard let imageData = compressImage(image, resolution: resolution) else {
                throw OCRError.imageCompressionFailed
            }

            // 调用 OCR 服务
            let result = try await performOCR(
                imageData: imageData,
                mode: mode,
                resolution: resolution
            )

            recognizedText = result
        } catch {
            errorMessage = error.localizedDescription
            recognizedText = "识别失败: \(error.localizedDescription)"
        }

        isProcessing = false
    }

    // 执行 OCR 请求
    private func performOCR(
        imageData: Data,
        mode: OCRMode,
        resolution: Resolution
    ) async throws -> String {

        // 构建请求
        let boundary = UUID().uuidString
        var request = URLRequest(url: URL(string: "\(serverURL)/api/ocr/image")!)
        request.httpMethod = "POST"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        // 构建 multipart body
        var body = Data()

        // 添加图片
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n".data(using: .utf8)!)

        // 添加模式
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"mode\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(mode.rawValue)\r\n".data(using: .utf8)!)

        // 添加分辨率
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"resolution\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(resolution.rawValue)x\(resolution.rawValue)\r\n".data(using: .utf8)!)

        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        // 发送请求
        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw OCRError.invalidResponse
        }

        guard httpResponse.statusCode == 200 else {
            throw OCRError.serverError(statusCode: httpResponse.statusCode)
        }

        // 解析响应
        let jsonResponse = try JSONDecoder().decode(OCRResponse.self, from: data)

        guard jsonResponse.success else {
            throw OCRError.recognitionFailed(jsonResponse.error ?? "未知错误")
        }

        return jsonResponse.text ?? ""
    }

    // 压缩图片
    private func compressImage(_ image: UIImage, resolution: Resolution) -> Data? {
        // 适配 iPhone 15 Pro Max 的屏幕尺寸
        let maxSize: CGFloat = 1500 // iPhone 15 Pro Max 宽度约为 430pt

        // 计算缩放比例
        let scale = min(maxSize / image.size.width, maxSize / image.size.height, 1.0)
        let newSize = CGSize(
            width: image.size.width * scale,
            height: image.size.height * scale
        )

        // 重新绘制图片
        UIGraphicsBeginImageContextWithOptions(newSize, false, 1.0)
        image.draw(in: CGRect(origin: .zero, size: newSize))
        let resizedImage = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()

        // 压缩质量
        let quality: CGFloat
        switch resolution {
        case .low: quality = 0.6
        case .medium: quality = 0.7
        case .high: quality = 0.8
        case .ultra: quality = 0.9
        }

        return resizedImage?.jpegData(compressionQuality: quality)
    }
}

// MARK: - 数据模型

struct OCRResponse: Codable {
    let success: Bool
    let text: String?
    let error: String?
    let mode: String?
    let processTime: String?

    enum CodingKeys: String, CodingKey {
        case success
        case text
        case error
        case mode
        case processTime = "process_time"
    }
}

// MARK: - 错误类型

enum OCRError: LocalizedError {
    case imageCompressionFailed
    case invalidResponse
    case serverError(statusCode: Int)
    case recognitionFailed(String)

    var errorDescription: String? {
        switch self {
        case .imageCompressionFailed:
            return "图片压缩失败"
        case .invalidResponse:
            return "服务器响应无效"
        case .serverError(let code):
            return "服务器错误 (代码: \(code))"
        case .recognitionFailed(let message):
            return "识别失败: \(message)"
        }
    }
}
