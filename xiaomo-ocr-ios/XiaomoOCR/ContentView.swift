//
//  XiaomoOCRApp.swift
//  小莫 OCR - iPhone 版本
//
//  专为 iPhone 15 Pro Max 优化
//

import SwiftUI

@main
struct XiaomoOCRApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

//
//  ContentView.swift
//  主界面
//

import SwiftUI
import PhotosUI

struct ContentView: View {
    @StateObject private var ocrManager = OCRManager()
    @State private var showImagePicker = false
    @State private var showCamera = false
    @State private var showSettings = false
    @State private var selectedMode: OCRMode = .general
    @State private var selectedResolution: Resolution = .high

    var body: some View {
        NavigationView {
            ZStack {
                // 渐变背景
                LinearGradient(
                    colors: [Color(hex: "667eea"), Color(hex: "764ba2")],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()

                ScrollView {
                    VStack(spacing: 25) {
                        // 顶部标题卡片
                        HeaderCard()
                            .padding(.top, 20)

                        // 快速操作按钮
                        QuickActionButtons(
                            showCamera: $showCamera,
                            showImagePicker: $showImagePicker
                        )

                        // 设置面板
                        SettingsPanel(
                            selectedMode: $selectedMode,
                            selectedResolution: $selectedResolution
                        )

                        // 识别结果
                        if ocrManager.isProcessing {
                            ProcessingView()
                        } else if !ocrManager.recognizedText.isEmpty {
                            ResultCard(text: ocrManager.recognizedText)
                        } else {
                            EmptyStateView()
                        }
                    }
                    .padding()
                }
            }
            .navigationBarHidden(true)
            .sheet(isPresented: $showImagePicker) {
                ImagePicker(sourceType: .photoLibrary) { image in
                    processImage(image)
                }
            }
            .sheet(isPresented: $showCamera) {
                ImagePicker(sourceType: .camera) { image in
                    processImage(image)
                }
            }
            .sheet(isPresented: $showSettings) {
                SettingsView()
            }
        }
    }

    private func processImage(_ image: UIImage) {
        Task {
            await ocrManager.recognizeText(
                from: image,
                mode: selectedMode,
                resolution: selectedResolution
            )
        }
    }
}

// MARK: - 组件

struct HeaderCard: View {
    var body: some View {
        VStack(spacing: 10) {
            // Logo
            Image(systemName: "doc.text.viewfinder")
                .font(.system(size: 60))
                .foregroundColor(.white)

            Text("小莫 OCR")
                .font(.system(size: 36, weight: .bold, design: .rounded))
                .foregroundColor(.white)

            Text("DeepSeek 智能文字识别")
                .font(.subheadline)
                .foregroundColor(.white.opacity(0.9))

            // 设备信息
            if UIDevice.current.userInterfaceIdiom == .phone {
                HStack {
                    Image(systemName: "iphone.gen3")
                    Text(UIDevice.current.name)
                }
                .font(.caption)
                .foregroundColor(.white.opacity(0.8))
                .padding(.top, 5)
            }
        }
        .padding(.vertical, 30)
    }
}

struct QuickActionButtons: View {
    @Binding var showCamera: Bool
    @Binding var showImagePicker: Bool

    var body: some View {
        HStack(spacing: 15) {
            // 拍照按钮
            ActionButton(
                icon: "camera.fill",
                title: "拍照识别",
                color: .white
            ) {
                showCamera = true
            }

            // 相册按钮
            ActionButton(
                icon: "photo.fill",
                title: "相册选择",
                color: .white
            ) {
                showImagePicker = true
            }
        }
        .padding(.horizontal)
    }
}

struct ActionButton: View {
    let icon: String
    let title: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.system(size: 40))
                    .foregroundColor(color)

                Text(title)
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundColor(color)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 25)
            .background(
                RoundedRectangle(cornerRadius: 20)
                    .fill(.white.opacity(0.2))
                    .overlay(
                        RoundedRectangle(cornerRadius: 20)
                            .stroke(.white.opacity(0.3), lineWidth: 1)
                    )
            )
        }
    }
}

struct SettingsPanel: View {
    @Binding var selectedMode: OCRMode
    @Binding var selectedResolution: Resolution

    var body: some View {
        VStack(spacing: 20) {
            // 识别模式
            VStack(alignment: .leading, spacing: 12) {
                Label("识别模式", systemImage: "wand.and.stars")
                    .font(.headline)
                    .foregroundColor(.white)

                HStack(spacing: 10) {
                    ForEach(OCRMode.allCases, id: \.self) { mode in
                        ModeButton(
                            mode: mode,
                            isSelected: selectedMode == mode
                        ) {
                            selectedMode = mode
                        }
                    }
                }
            }

            // 分辨率
            VStack(alignment: .leading, spacing: 12) {
                Label("识别精度", systemImage: "slider.horizontal.3")
                    .font(.headline)
                    .foregroundColor(.white)

                HStack(spacing: 10) {
                    ForEach(Resolution.allCases, id: \.self) { resolution in
                        ResolutionButton(
                            resolution: resolution,
                            isSelected: selectedResolution == resolution
                        ) {
                            selectedResolution = resolution
                        }
                    }
                }
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(.white.opacity(0.15))
        )
        .padding(.horizontal)
    }
}

struct ModeButton: View {
    let mode: OCRMode
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 6) {
                Image(systemName: mode.icon)
                    .font(.system(size: 22))

                Text(mode.title)
                    .font(.caption)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 12)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(isSelected ? .white : .white.opacity(0.2))
            )
            .foregroundColor(isSelected ? Color(hex: "667eea") : .white)
        }
    }
}

struct ResolutionButton: View {
    let resolution: Resolution
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(resolution.title)
                .font(.system(size: 14, weight: .semibold))
                .frame(maxWidth: .infinity)
                .padding(.vertical, 10)
                .background(
                    RoundedRectangle(cornerRadius: 10)
                        .fill(isSelected ? .white : .white.opacity(0.2))
                )
                .foregroundColor(isSelected ? Color(hex: "667eea") : .white)
        }
    }
}

struct ProcessingView: View {
    var body: some View {
        VStack(spacing: 20) {
            ProgressView()
                .scaleEffect(1.5)
                .tint(.white)

            Text("正在识别中...")
                .font(.headline)
                .foregroundColor(.white)

            Text("请稍候，AI 正在分析图片")
                .font(.subheadline)
                .foregroundColor(.white.opacity(0.8))
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 60)
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(.white.opacity(0.15))
        )
        .padding(.horizontal)
    }
}

struct ResultCard: View {
    let text: String
    @State private var showShareSheet = false

    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            HStack {
                Label("识别结果", systemImage: "checkmark.circle.fill")
                    .font(.headline)
                    .foregroundColor(.white)

                Spacer()

                Button(action: { showShareSheet = true }) {
                    Image(systemName: "square.and.arrow.up")
                        .foregroundColor(.white)
                }
            }

            ScrollView {
                Text(text)
                    .font(.body)
                    .foregroundColor(.white)
                    .textSelection(.enabled)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .frame(maxHeight: 300)

            HStack(spacing: 10) {
                Button(action: {
                    UIPasteboard.general.string = text
                }) {
                    Label("复制", systemImage: "doc.on.doc")
                        .font(.subheadline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                        .background(
                            RoundedRectangle(cornerRadius: 10)
                                .fill(.white.opacity(0.2))
                        )
                }
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(.white.opacity(0.15))
        )
        .padding(.horizontal)
        .sheet(isPresented: $showShareSheet) {
            ShareSheet(items: [text])
        }
    }
}

struct EmptyStateView: View {
    var body: some View {
        VStack(spacing: 15) {
            Image(systemName: "doc.text.magnifyingglass")
                .font(.system(size: 60))
                .foregroundColor(.white.opacity(0.6))

            Text("开始识别")
                .font(.title2.bold())
                .foregroundColor(.white)

            Text("点击上方按钮拍照或选择图片")
                .font(.subheadline)
                .foregroundColor(.white.opacity(0.8))
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 60)
    }
}

// MARK: - 模型定义

enum OCRMode: String, CaseIterable {
    case general = "general"
    case document = "doc2md"
    case figure = "figure"

    var title: String {
        switch self {
        case .general: return "通用"
        case .document: return "文档"
        case .figure: return "图表"
        }
    }

    var icon: String {
        switch self {
        case .general: return "doc.text"
        case .document: return "doc.richtext"
        case .figure: return "chart.bar"
        }
    }
}

enum Resolution: String, CaseIterable {
    case low = "512"
    case medium = "768"
    case high = "1024"
    case ultra = "1280"

    var title: String {
        switch self {
        case .low: return "快速"
        case .medium: return "均衡"
        case .high: return "高清"
        case .ultra: return "极致"
        }
    }

    var value: Int {
        Int(rawValue) ?? 1024
    }
}

// MARK: - 辅助视图

struct ShareSheet: UIViewControllerRepresentable {
    let items: [Any]

    func makeUIViewController(context: Context) -> UIActivityViewController {
        UIActivityViewController(activityItems: items, applicationActivities: nil)
    }

    func updateUIViewController(_ uiViewController: UIActivityViewController, context: Context) {}
}

// MARK: - 颜色扩展

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3:
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}
