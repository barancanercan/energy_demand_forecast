import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center">
      <div className="max-w-lg p-8 bg-gray-900 rounded-lg shadow-xl text-center">
        <h1 className="text-4xl font-bold mb-6 text-blue-500">Enerji Tahmin Uygulaması</h1>
        <p className="mb-8 text-gray-300">
          Gelişmiş makine öğrenmesi modellerini kullanarak enerji yükünü tahmin edin.
        </p>
        <div className="space-x-4">
          <Link
            href="/predict"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
          >
            Tahmin Yap
          </Link>
          <Link
            href="/forecast"
            className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition"
          >
            Tahminleri Görüntüle
          </Link>
        </div>
      </div>
    </div>
  )
}