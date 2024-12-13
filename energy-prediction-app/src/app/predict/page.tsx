'use client'
import { useState } from "react";

export default function PredictPage() {
  const [formData, setFormData] = useState({
    generation_biomass: '',
    generation_fossil_brown_coal_lignite: '',
    generation_fossil_coal_derived_gas: '',
    generation_fossil_gas: '',
    generation_fossil_hard_coal: '',
    generation_fossil_oil: '',
    generation_geothermal: '',
    generation_hydro_pumped_storage_consumption: '',
    generation_hydro_run_of_river_and_poundage: '',
    generation_hydro_water_reservoir: '',
    generation_solar: '',
    generation_wind_onshore: '',
    forecast_solar_day_ahead: '',
    forecast_wind_onshore_day_ahead: '',
    total_load_forecast: '',
    hour: '',
    day_of_week: '',
    month: '',
    is_weekend: '',
    season: ''
  });

  const [result, setResult] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setResult(null);

    const payload = Object.fromEntries(
      Object.entries(formData).map(([key, value]) => [key, Number(value)])
    );

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Tahmin sırasında bir hata oluştu");
      }

      const data = await response.json();
      setResult(data.prediction);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-800 via-black to-gray-900 text-white">
      <div className="max-w-3xl w-full p-8 bg-gray-900 rounded-lg shadow-2xl">
        <h1 className="text-4xl font-bold text-center mb-6 text-blue-400">
          Enerji Tahmini Formu
        </h1>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.entries(formData).map(([key, value]) => (
            <div key={key} className="flex flex-col">
              <label htmlFor={key} className="mb-2 font-semibold text-gray-200">
                {key.replace(/_/g, ' ')}
              </label>
              <input
                type="number"
                id={key}
                name={key}
                value={value}
                onChange={handleInputChange}
                step="0.1"
                placeholder={`${key.replace(/_/g, ' ')} girin`}
                className="w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-100 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-400"
                required
              />
            </div>
          ))}
          <div className="col-span-full">
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-3 rounded-lg text-lg font-semibold ${
                isLoading
                  ? "bg-gray-600 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700 transition"
              } text-white`}
            >
              {isLoading ? "Tahmin Ediliyor..." : "Tahmin Yap"}
            </button>
          </div>
        </form>

        {isLoading && (
          <div className="mt-6 text-center">
            <p className="text-blue-400 font-semibold">Tahmin işlemi devam ediyor...</p>
          </div>
        )}

        {result !== null && (
          <div className="mt-6 p-4 text-center bg-green-800 rounded-lg shadow-md">
            <p className="text-xl font-bold text-green-200">Tahmin Sonucu: {result.toFixed(2)}</p>
          </div>
        )}

        {error && (
          <div className="mt-6 p-4 text-center bg-red-800 rounded-lg shadow-md">
            <p className="text-red-200 font-semibold">Hata: {error}</p>
          </div>
        )}
      </div>
    </div>
  );
}
