//
//  SettingsView.swift
//  设置界面
//

import SwiftUI

struct SettingsView: View {
    @AppStorage("serverURL") private var serverURL = "http://localhost:5000"
    @AppStorage("useLocalServer") private var useLocalServer = true
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationView {
            Form {
                Section {
                    HStack {
                        Image(systemName: "iphone.gen3")
                            .font(.largeTitle)
                            .foregroundColor(Color(hex: "667eea"))

                        VStack(alignment: .leading) {
                            Text("小莫 OCR")
                                .font(.title2.bold())

                            Text("iPhone 专用版本")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    }
                    .padding(.vertical, 10)
                }

                Section(header: Text("服务器设置")) {
                    Toggle("使用本地服务器", isOn: $useLocalServer)
                        .tint(Color(hex: "667eea"))

                    if useLocalServer {
                        HStack {
                            Text("服务器地址")
                            Spacer()
                            TextField("URL", text: $serverURL)
                                .multilineTextAlignment(.trailing)
                                .textInputAutocapitalization(.never)
                                .autocorrectionDisabled()
                        }

                        Button(action: testConnection) {
                            Label("测试连接", systemImage: "network")
                        }
                    }
                }

                Section(header: Text("推荐配置")) {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("方案一：本地 Mac 服务器")
                            .font(.headline)

                        Text("1. 在同一 WiFi 下的 Mac 上运行服务器")
                        Text("2. 将服务器地址改为 Mac 的 IP")
                        Text("   例如: http://192.168.1.100:5000")

                        Divider()

                        Text("方案二：使用 Web 版本")
                            .font(.headline)

                        Text("使用 Safari 访问响应式 Web 版本")
                            .foregroundColor(.secondary)
                    }
                    .font(.caption)
                    .padding(.vertical, 5)
                }

                Section(header: Text("设备信息")) {
                    InfoRow(title: "设备型号", value: UIDevice.current.name)
                    InfoRow(title: "系统版本", value: "iOS \(UIDevice.current.systemVersion)")
                    InfoRow(title: "屏幕尺寸", value: getScreenSize())
                }

                Section(header: Text("关于")) {
                    Link(destination: URL(string: "https://github.com/deepseek-ai/DeepSeek-OCR")!) {
                        HStack {
                            Text("DeepSeek-OCR GitHub")
                            Spacer()
                            Image(systemName: "arrow.up.right")
                        }
                    }

                    HStack {
                        Text("版本")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }
                }
            }
            .navigationTitle("设置")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("完成") {
                        dismiss()
                    }
                }
            }
        }
    }

    private func testConnection() {
        // TODO: 实现连接测试
    }

    private func getScreenSize() -> String {
        let screen = UIScreen.main.bounds
        return "\(Int(screen.width)) × \(Int(screen.height)) pt"
    }
}

struct InfoRow: View {
    let title: String
    let value: String

    var body: some View {
        HStack {
            Text(title)
            Spacer()
            Text(value)
                .foregroundColor(.secondary)
        }
    }
}
