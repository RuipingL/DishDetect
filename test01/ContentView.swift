import SwiftUI
import AVFoundation
import Foundation

struct ResponseData: Codable {
    var description: String
    var speech_url: String
}
import SwiftUI
import AVFoundation




struct ContentView: View {
    @State private var image: UIImage? = nil
    @State private var showImagePicker: Bool = false
    @State private var isProcessing: Bool = false
    @State private var descriptionText: String = ""
    @State private var audioPlayer: AVAudioPlayer?
    @State private var speechSynthesizer = AVSpeechSynthesizer()
    var body: some View {
        VStack {
            if let image = image {
                Image(uiImage: image)
                    .resizable()
                    .scaledToFit()
                    .onTapGesture {
                        self.showImagePicker = true
                    }
            } else {
                Button(action: {
                    self.showImagePicker = true
                }) {
                    Text("Take a Photo")
                        .font(.largeTitle)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
            }
            
            if isProcessing {
                Text("Please wait...")
                    .font(.headline)
                    .padding()
            }

            Text(descriptionText)
                .padding()
        }
        .sheet(isPresented: $showImagePicker, onDismiss: processImage) {
            ImagePicker(image: self.$image)
        }
    }
    
    func speak(description: String) {
        let utterance = AVSpeechUtterance(string: description)
        utterance.voice = AVSpeechSynthesisVoice(language: "en-US")  // 或者选择合适的语言，例如"zh-CN"对于中文
        utterance.rate = 0.5  // 你可以调整说话速度

        speechSynthesizer.speak(utterance)
    }

    
    func processImage() {
        guard let image = image else { return }
        isProcessing = true
        let resizedImage = resizeImage(image: image, targetSize: CGSize(width: 640, height: 480))
        uploadImage(image: resizedImage)
    }

    func uploadImage(image: UIImage) {
        guard let imageData = image.jpegData(compressionQuality: 0.5) else { return }
        guard let url = URL(string: "http://141.3.14.41:5000/process-image") else { return }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 300 // Set request timeout interval to 300 seconds (5 minutes)
        config.timeoutIntervalForResource = 300 // Set resource timeout interval to 300 seconds (5 minutes)

        let session = URLSession(configuration: config)
        session.uploadTask(with: request, from: body) { data, response, error in
            guard let data = data, error == nil else {
                print("Error: \(String(describing: error))")
                DispatchQueue.main.async {
                    self.isProcessing = false
                }
                return
            }
            self.handleResponse(data: data)  // Using the handleResponse function to process the data
        }.resume()
    }


    func handleResponse(data: Data) {
        do {
            let responseData = try JSONDecoder().decode(ResponseData.self, from: data)
            DispatchQueue.main.async {
                self.descriptionText = responseData.description
                self.isProcessing = false
                self.speak(description: self.descriptionText)  // 调用朗读函数
            }
        } catch {
            print("Error decoding response: \(error)")
            DispatchQueue.main.async {
                self.isProcessing = false
            }
        }
    }



    func resizeImage(image: UIImage, targetSize: CGSize) -> UIImage {
        let size = image.size

        let widthRatio  = targetSize.width  / size.width
        let heightRatio = targetSize.height / size.height
        var newSize: CGSize
        if widthRatio > heightRatio {
            newSize = CGSize(width: size.width * heightRatio, height: size.height * heightRatio)
        } else {
            newSize = CGSize(width: size.width * widthRatio, height: size.height * widthRatio)
        }

        UIGraphicsBeginImageContextWithOptions(newSize, false, 1.0)
        image.draw(in: CGRect(x: 0, y: 0, width: newSize.width, height: newSize.height))
        let newImage = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()

        return newImage!
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
