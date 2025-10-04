'use client'

import { useState } from 'react';

export default function LanguageConverter() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState<{ text: string; romaji: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleConvert = async () => {
    if (!inputText.trim()) return;
    
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText })
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error('変換エラー:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-gray-900 dark:to-indigo-900 flex flex-col items-center justify-center p-4">
      {/* 头部标题 */}
      <div className="w-full max-w-3xl mb-8 text-center animate-fade-in">
        <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 mb-2">
          Language Converter
        </h1>
        <p className="text-gray-600 dark:text-gray-300 text-lg">
          英語や中国語を日本語とローマ字に変換します
        </p>
      </div>

      {/* 主内容区 */}
      <div className="w-full max-w-3xl bg-white dark:bg-gray-800 rounded-xl shadow-xl p-6 md:p-8 transition-all duration-300 hover:shadow-2xl">
        {/* 输入区域 */}
        <div className="mb-6 space-y-4">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="ここに英語または中国語のテキストを入力してください..."
            className="w-full min-h-[120px] p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 resize-none bg-gray-50 dark:bg-gray-700 dark:text-white"
          />
          <button 
            onClick={handleConvert} 
            disabled={loading || !inputText.trim()}
            className={`px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-lg transition-all duration-300 transform hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none disabled:transform-none flex items-center justify-center gap-2 ${inputText.trim() ? '' : 'cursor-not-allowed'}`}
          >
            {loading ? (
              <> 
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                変換中...
              </>
            ) : '変換'}
          </button>
        </div>

        {/* 结果区域 */}
        {result && (
          <div className="result-area bg-gray-50 dark:bg-gray-700 rounded-lg p-5 border-l-4 border-indigo-500 animate-fade-in-up">
            <h2 className="text-xl font-semibold mb-3 text-gray-800 dark:text-white">変換結果</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">日本語</h3>
                <div className="text-lg md:text-xl leading-relaxed text-gray-900 dark:text-white font-medium">
                  {result.text}
                </div>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">ローマ字</h3>
                <div className="text-base font-mono text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 p-3 rounded-md">
                  {result.romaji}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 页脚 */}
      <div className="mt-8 text-gray-500 dark:text-gray-400 text-sm">
        Language Converter © {new Date().getFullYear()}
      </div>
    </div>
  );
}
