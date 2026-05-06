#!/usr/bin/env python3
# main.py - Herramienta completa para manipular data.csz y EBOOT.PBP de Cave Story PSP
# Versión 1.0.0
# Original por andwhyisit | Porteado a Python por EdwarlyGamer999+
# Detección automática del idioma del sistema


import os
import sys
import zlib
import struct
import re
import zipfile
import shutil
import time
import locale
from tkinter import *
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading

# ------------------------------------------------------------
# Configuración de idiomas
# ------------------------------------------------------------
LANGUAGES = {
    'en': {
        'name': 'English 🇬🇧',
        'app_title': 'Cave Story CSZ Tools+ v1.0.0',
        'credit': 'CSZ Tools+ v1.0.0\nOriginal tool by andwhyisit | Python port by EdwarlyGamer999+',
        'btn_full': 'Extract All (data.csz → data folder) [adds (1)/(2)]',
        'btn_en': 'Extract English (data.csz → data folder)',
        'btn_jp': 'Extract Japanese (data.csz → data folder)',
        'btn_compress': 'Compress (data folder → data.csz)',
        'btn_restore': 'Restore original data.csz (from ZIP)',
        'btn_patch': 'Apply Patch/Mod to Cave Story PSP',
        'btn_extract_eboot': 'Extract EBOOT.PBP',
        'btn_compress_eboot': 'Compress EBOOT.PBP',
        'btn_edit_param': 'Edit PARAM.SFO',
        'btn_restore_eboot': 'Restore Original EBOOT.PBP',
        'btn_copy_log': 'Copy Log',
        'btn_clear_log': 'Clear Log',
        'log_full_start': 'Extracting all (with suffixes) from {0} to {1}...',
        'log_en_start': 'Extracting English from {0} to {1}...',
        'log_jp_start': 'Extracting Japanese from {0} to {1}...',
        'log_compress_start': 'Packing folder {0}...',
        'log_compress_ok': 'Archive generated: {0} bytes, {1} files',
        'log_compress_compressed': 'Compressed: {0} -> {1} bytes',
        'log_compress_log': 'Log generated: archive.dat',
        'log_compress_clean': 'Folder {0} deleted.',
        'log_compress_keep': 'Folder {0} kept.',
        'log_restore_start': 'Restoring from {0}...',
        'log_restore_ok': 'Restoration completed. The data.csz file should be identical to the original.',
        'log_restore_crc': 'Restored {0} (CRC: 0x{1:08X})',
        'log_restore_warn': 'WARNING: CRC does not match the expected original.',
        'log_cancelled': 'Operation cancelled by user.',
        'log_copied': 'Log copied to clipboard.',
        'log_cleared': 'Log cleared.',
        'err_no_csz': 'No data.csz found in current directory. Select manually?',
        'err_no_dir': 'Folder "{0}" does not exist. Select another folder?',
        'err_no_zip': 'No ZIP file found. Select manually?',
        'err_no_files': 'No files in folder',
        'err_decompress': 'Decompression error: {0}',
        'err_incomplete': 'Incomplete header',
        'err_small': 'File too small',
        'err_no_english': 'No English files found in the archive.',
        'err_no_japanese': 'No Japanese files found in the archive.',
        'confirm_restore': 'Restore original data.csz? The current file will be overwritten.',
        'confirm_clean': 'Delete folder "{0}" after compression?',
        'confirm_extract_english': 'Extract English files?',
        'confirm_extract_english_msg': 'This will overwrite the "data" folder if it exists. Continue?',
        'confirm_extract_japanese': 'Extract Japanese files?',
        'confirm_extract_japanese_msg': 'This will overwrite the "data" folder if it exists. Continue?',
        'confirm_extract_all': 'Extract all files?',
        'confirm_extract_all_msg': 'This will overwrite the "data" folder if it exists. Continue?',
        'confirm_compress': 'Compress folder?',
        'confirm_compress_msg': 'This will create a new data.csz file. The existing one will be overwritten. Continue?',
        'ask_manual_csz': 'data.csz not found in current directory. Do you want to select it manually?',
        'ask_manual_dir': 'Folder "{0}" does not exist. Do you want to select another folder?',
        'ask_manual_zip': 'data_original.zip not found. Select ZIP file manually?',
        'compress_result': 'Compressed file size:',
        'lang_english': 'English only',
        'lang_japanese': 'Japanese only',
        'lang_both': 'Both English and Japanese',
        'lang_neutral': 'Neutral (no specific language)',
        'help_title': 'Help - CSZ Tools',
        'help_close': 'Close',
        'patch_select_eboot': 'Select EBOOT.PBP file',
        'patch_select_csz': 'Select data.csz file to apply',
        'patch_copying': 'Copying {0} to {1}...',
        'patch_success': 'Patch applied successfully. data.csz replaced.',
        'patch_cancel': 'Operation cancelled by user.',
        'patch_wrong_title': 'The selected EBOOT.PBP is not Cave Story (title: "{0}"). Operation cancelled.',
        'patch_recognized': 'Cave Story recognized correctly.',
        'patch_csz_not_found': 'No data.csz selected.',
        'patch_io_error': 'Error reading EBOOT.PBP: {0}',
        'patch_error_title': 'Invalid Game',
        'extract_eboot_title': 'Extract EBOOT.PBP',
        'extract_eboot_select': 'Select EBOOT.PBP file to extract',
        'extract_eboot_start': 'Extracting EBOOT.PBP to {0}...',
        'extract_eboot_success': 'EBOOT.PBP extracted successfully.',
        'extract_eboot_title_dialog': 'Game title: "{0}"\nExtract anyway?',
        'extract_eboot_warning': 'It is advisable to modify the game name.\nModify other parameters at your own risk.',
        'extract_eboot_missing': 'No files extracted (maybe empty sections).',
        'compress_eboot_title': 'Compress EBOOT.PBP',
        'compress_eboot_select_dir': 'Select folder containing extracted EBOOT files',
        'compress_eboot_checking': 'Checking folder {0}...',
        'compress_eboot_missing_data_psp': 'DATA.PSP not found in the selected folder.',
        'compress_eboot_missing_pic1': 'PIC1.PNG not found in the selected folder.',
        'compress_eboot_success': 'EBOOT.PBP generated successfully.',
        'compress_eboot_saved': 'Saved as: {0}',
        'compress_eboot_error': 'Error during compression: {0}',
        'btn_edit_param': 'Edit PARAM.SFO',
        'edit_param_title': 'Edit PARAM.SFO - Game Title',
        'edit_param_select_folder': 'Select folder containing PARAM.SFO',
        'edit_param_not_found': 'PARAM.SFO not found in the selected folder.',
        'edit_param_error': 'Error',
        'edit_param_current': 'Current title:',
        'edit_param_new': 'New title:',
        'edit_param_warning': 'For detailed editing of this file, use an external program. This tool only changes the game name quickly.',
        'edit_param_long_warning': 'If the name is too long, it could crash or cause unexpected errors. Proceed at your own risk.',
        'edit_param_empty': 'Title cannot be empty.',
        'edit_param_too_long': 'The new title is too long for the space reserved in PARAM.SFO. Use an external editor.',
        'edit_param_success': 'Title updated successfully.',
        'edit_param_save': 'Save',
        'btn_restore_eboot': 'Restore Original EBOOT.PBP',
        'restore_eboot_title': 'Restore Original EBOOT.PBP',
        'restore_eboot_select_zip': 'Select ZIP file containing original EBOOT.PBP',
        'restore_eboot_checking': 'Restoring EBOOT.PBP from {0}...',
        'restore_eboot_success': 'EBOOT.PBP restored successfully.',
        'restore_eboot_crc_match': 'CRC32 matches the original.',
        'restore_eboot_crc_mismatch': 'CRC32 does NOT match the original. The file may be modified.',
        'restore_eboot_no_csz': 'No EBOOT.PBP found in the ZIP.',
        'restore_eboot_error': 'Error during restoration: {0}',
    },
    'es': {
        'name': 'Español 🇪🇸',
        'app_title': 'Cave Story CSZ Tools+ v1.0.0',
        'credit': 'CSZ Tools+ v1.0.0\nHerramienta original por andwhyisit | Porteado a Python por EdwarlyGamer999+',
        'btn_full': 'Extraer Completo (data.csz → carpeta data) [añade (1)/(2)]',
        'btn_en': 'Extraer Inglés (data.csz → carpeta data)',
        'btn_jp': 'Extraer Japonés (data.csz → carpeta data)',
        'btn_compress': 'Comprimir (carpeta data → data.csz)',
        'btn_restore': 'Restaurar data.csz original (desde ZIP)',
        'btn_patch': 'Aplicar Parche/Mod a Cave Story PSP',
        'btn_extract_eboot': 'Extraer EBOOT.PBP',
        'btn_compress_eboot': 'Comprimir EBOOT.PBP',
        'btn_edit_param': 'Editar PARAM.SFO',
        'btn_restore_eboot': 'Restaurar EBOOT.PBP Original',
        'btn_copy_log': 'Copiar Log',
        'btn_clear_log': 'Limpiar Log',
        'log_full_start': 'Extrayendo completo (con sufijos) desde {0} a {1}...',
        'log_en_start': 'Extrayendo inglés desde {0} a {1}...',
        'log_jp_start': 'Extrayendo japonés desde {0} a {1}...',
        'log_compress_start': 'Empaquetando carpeta {0}...',
        'log_compress_ok': 'Archivo generado: {0} bytes, {1} archivos',
        'log_compress_compressed': 'Comprimido: {0} -> {1} bytes',
        'log_compress_log': 'Log generado: archive.dat',
        'log_compress_clean': 'Carpeta {0} eliminada.',
        'log_compress_keep': 'Carpeta {0} conservada.',
        'log_restore_start': 'Restaurando desde {0}...',
        'log_restore_ok': 'Restauración completada. El archivo data.csz debería ser idéntico al original.',
        'log_restore_crc': 'Restaurado {0} (CRC: 0x{1:08X})',
        'log_restore_warn': 'ADVERTENCIA: El CRC no coincide con el original esperado.',
        'log_cancelled': 'Operación cancelada por el usuario.',
        'log_copied': 'Log copiado al portapapeles.',
        'log_cleared': 'Log limpiado.',
        'err_no_csz': 'No se encuentra data.csz en el directorio actual. ¿Seleccionar manualmente?',
        'err_no_dir': 'La carpeta "{0}" no existe. ¿Seleccionar otra carpeta?',
        'err_no_zip': 'No se encuentra archivo ZIP. ¿Seleccionar manualmente?',
        'err_no_files': 'No hay archivos en la carpeta',
        'err_decompress': 'Error de descompresión: {0}',
        'err_incomplete': 'Cabecera incompleta',
        'err_small': 'Archivo demasiado pequeño',
        'err_no_english': 'No se encontraron archivos en inglés en el archivo.',
        'err_no_japanese': 'No se encontraron archivos en japonés en el archivo.',
        'confirm_restore': '¿Restaurar data.csz original? Se sobrescribirá el archivo actual.',
        'confirm_clean': '¿Borrar la carpeta "{0}" después de comprimir?',
        'confirm_extract_english': '¿Extraer archivos en inglés?',
        'confirm_extract_english_msg': 'Esto sobrescribirá la carpeta "data" si existe. ¿Continuar?',
        'confirm_extract_japanese': '¿Extraer archivos en japonés?',
        'confirm_extract_japanese_msg': 'Esto sobrescribirá la carpeta "data" si existe. ¿Continuar?',
        'confirm_extract_all': '¿Extraer todos los archivos?',
        'confirm_extract_all_msg': 'Esto sobrescribirá la carpeta "data" si existe. ¿Continuar?',
        'confirm_compress': '¿Comprimir carpeta?',
        'confirm_compress_msg': 'Esto creará un nuevo archivo data.csz. Se sobrescribirá el existente. ¿Continuar?',
        'ask_manual_csz': 'No se encuentra data.csz en el directorio actual. ¿Deseas seleccionarlo manualmente?',
        'ask_manual_dir': 'La carpeta "{0}" no existe. ¿Deseas seleccionar otra carpeta?',
        'ask_manual_zip': 'No se encuentra data_original.zip. ¿Seleccionar archivo ZIP manualmente?',
        'compress_result': 'Tamaño del archivo comprimido:',
        'lang_english': 'Solo inglés',
        'lang_japanese': 'Solo japonés',
        'lang_both': 'Inglés y japonés',
        'lang_neutral': 'Neutral (sin idioma específico)',
        'help_title': 'Ayuda - CSZ Tools',
        'help_close': 'Cerrar',
        'patch_select_eboot': 'Seleccionar archivo EBOOT.PBP',
        'patch_select_csz': 'Seleccionar archivo data.csz a aplicar',
        'patch_copying': 'Copiando {0} a {1}...',
        'patch_success': 'Parche aplicado correctamente. data.csz reemplazado.',
        'patch_cancel': 'Operación cancelada por el usuario.',
        'patch_wrong_title': 'El EBOOT.PBP seleccionado no es Cave Story (título: "{0}"). Operación cancelada.',
        'patch_recognized': 'Cave Story reconocido correctamente.',
        'patch_csz_not_found': 'No se seleccionó ningún data.csz.',
        'patch_io_error': 'Error al leer EBOOT.PBP: {0}',
        'patch_error_title': 'Juego inválido',
        'extract_eboot_title': 'Extraer EBOOT.PBP',
        'extract_eboot_select': 'Seleccionar archivo EBOOT.PBP a extraer',
        'extract_eboot_start': 'Extrayendo EBOOT.PBP a {0}...',
        'extract_eboot_success': 'EBOOT.PBP extraído correctamente.',
        'extract_eboot_title_dialog': 'Título del juego: "{0}"\n¿Extraer de todas formas?',
        'extract_eboot_warning': 'Es sugerible modificar el nombre del juego.\nModifica los demás parámetros bajo tu propio riesgo.',
        'extract_eboot_missing': 'No se extrajeron archivos (quizás secciones vacías).',
        'compress_eboot_title': 'Comprimir EBOOT.PBP',
        'compress_eboot_select_dir': 'Seleccionar carpeta con los archivos extraídos de EBOOT',
        'compress_eboot_checking': 'Verificando carpeta {0}...',
        'compress_eboot_missing_data_psp': 'No se encuentra DATA.PSP en la carpeta seleccionada.',
        'compress_eboot_missing_pic1': 'No se encuentra PIC1.PNG en la carpeta seleccionada.',
        'compress_eboot_success': 'EBOOT.PBP generado correctamente.',
        'compress_eboot_saved': 'Guardado como: {0}',
        'compress_eboot_error': 'Error durante la compresión: {0}',
        'btn_edit_param': 'Editar PARAM.SFO',
        'edit_param_title': 'Editar PARAM.SFO - Título del juego',
        'edit_param_select_folder': 'Seleccionar carpeta que contenga PARAM.SFO',
        'edit_param_not_found': 'No se encontró PARAM.SFO en la carpeta seleccionada.',
        'edit_param_error': 'Error',
        'edit_param_current': 'Título actual:',
        'edit_param_new': 'Nuevo título:',
        'edit_param_warning': 'Para modificar este archivo a detalle use un programa externo. Esto es para editar el nombre rápidamente sin instalar nada más.',
        'edit_param_long_warning': 'Si el nombre es muy extenso podría llegar a crashear o podrían ocurrir errores inesperados, prosiga bajo su propio riesgo.',
        'edit_param_empty': 'El título no puede estar vacío.',
        'edit_param_too_long': 'El nuevo título es demasiado largo para el espacio reservado en PARAM.SFO. Use un editor externo.',
        'edit_param_success': 'Título actualizado correctamente.',
        'edit_param_save': 'Guardar',
        'btn_restore_eboot': 'Restaurar EBOOT.PBP Original',
        'restore_eboot_title': 'Restaurar EBOOT.PBP Original',
        'restore_eboot_select_zip': 'Seleccionar archivo ZIP que contenga el EBOOT.PBP original',
        'restore_eboot_checking': 'Restaurando EBOOT.PBP desde {0}...',
        'restore_eboot_success': 'EBOOT.PBP restaurado correctamente.',
        'restore_eboot_crc_match': 'El CRC32 coincide con el original.',
        'restore_eboot_crc_mismatch': 'El CRC32 NO coincide con el original. El archivo puede estar modificado.',
        'restore_eboot_no_csz': 'No se encontró EBOOT.PBP en el ZIP.',
        'restore_eboot_error': 'Error durante la restauración: {0}',
    },
    'jp': {
        'name': '日本語 🇯🇵',
        'app_title': 'Cave Story CSZ Tools+ v1.0.0',
        'credit': 'CSZ Tools+ v1.0.0\nオリジナルツール by andwhyisit | Python移植 by EdwarlyGamer999+',
        'btn_full': 'すべて抽出 (data.csz → dataフォルダ) [サフィックス (1)(2) 追加]',
        'btn_en': '英語抽出 (data.csz → dataフォルダ)',
        'btn_jp': '日本語抽出 (data.csz → dataフォルダ)',
        'btn_compress': '圧縮 (dataフォルダ → data.csz)',
        'btn_restore': '元のdata.cszを復元 (ZIPから)',
        'btn_patch': 'パッチ/ModをCave Story PSPに適用',
        'btn_extract_eboot': 'EBOOT.PBPを抽出',
        'btn_compress_eboot': 'EBOOT.PBPを圧縮',
        'btn_edit_param': 'PARAM.SFOを編集',
        'btn_restore_eboot': '元のEBOOT.PBPを復元',
        'btn_copy_log': 'ログをコピー',
        'btn_clear_log': 'ログをクリア',
        'log_full_start': '{0}から{1}にすべて抽出中（サフィックス付き）...',
        'log_en_start': '{0}から英語を{1}に抽出中...',
        'log_jp_start': '{0}から日本語を{1}に抽出中...',
        'log_compress_start': 'フォルダ{0}をパック中...',
        'log_compress_ok': 'アーカイブ生成: {0} バイト, {1} ファイル',
        'log_compress_compressed': '圧縮: {0} -> {1} バイト',
        'log_compress_log': 'ログ生成: archive.dat',
        'log_compress_clean': 'フォルダ{0}を削除しました。',
        'log_compress_keep': 'フォルダ{0}を保持しました。',
        'log_restore_start': '{0}から復元中...',
        'log_restore_ok': '復元完了。data.cszはオリジナルと同一であるはずです。',
        'log_restore_crc': '復元: {0} (CRC: 0x{1:08X})',
        'log_restore_warn': '警告: CRCが期待されるオリジナルと一致しません。',
        'log_cancelled': 'ユーザーにより操作がキャンセルされました。',
        'log_copied': 'ログをクリップボードにコピーしました。',
        'log_cleared': 'ログをクリアしました。',
        'err_no_csz': 'カレントディレクトリにdata.cszが見つかりません。手動で選択しますか？',
        'err_no_dir': 'フォルダ"{0}"が存在しません。別のフォルダを選択しますか？',
        'err_no_zip': 'ZIPファイルが見つかりません。手動で選択しますか？',
        'err_no_files': 'フォルダ内にファイルがありません',
        'err_decompress': '解凍エラー: {0}',
        'err_incomplete': 'ヘッダが不完全です',
        'err_small': 'ファイルが小さすぎます',
        'err_no_english': 'アーカイブ内に英語ファイルが見つかりません。',
        'err_no_japanese': 'アーカイブ内に日本語ファイルが見つかりません。',
        'confirm_restore': '元のdata.cszを復元しますか？現在のファイルは上書きされます。',
        'confirm_clean': '圧縮後にフォルダ"{0}"を削除しますか？',
        'confirm_extract_english': '英語ファイルを抽出しますか？',
        'confirm_extract_english_msg': '「data」フォルダが存在する場合は上書きされます。続行しますか？',
        'confirm_extract_japanese': '日本語ファイルを抽出しますか？',
        'confirm_extract_japanese_msg': '「data」フォルダが存在する場合は上書きされます。続行しますか？',
        'confirm_extract_all': 'すべてのファイルを抽出しますか？',
        'confirm_extract_all_msg': '「data」フォルダが存在する場合は上書きされます。続行しますか？',
        'confirm_compress': 'フォルダを圧縮しますか？',
        'confirm_compress_msg': '新しいdata.cszファイルを作成します。既存のファイルは上書きされます。続行しますか？',
        'ask_manual_csz': 'カレントディレクトリにdata.cszがありません。手動で選択しますか？',
        'ask_manual_dir': 'フォルダ"{0}"が存在しません。別のフォルダを選択しますか？',
        'ask_manual_zip': 'data_original.zipが見つかりません。手動でZIPファイルを選択しますか？',
        'compress_result': '圧縮ファイルサイズ:',
        'lang_english': '英語のみ',
        'lang_japanese': '日本語のみ',
        'lang_both': '英語と日本語',
        'lang_neutral': 'ニュートラル（言語なし）',
        'help_title': 'ヘルプ - CSZ Tools',
        'help_close': '閉じる',
        'patch_select_eboot': 'EBOOT.PBPファイルを選択',
        'patch_select_csz': '適用するdata.cszファイルを選択',
        'patch_copying': '{0} を {1} にコピー中...',
        'patch_success': 'パッチ適用成功。data.cszを置き換えました。',
        'patch_cancel': 'ユーザーにより操作がキャンセルされました。',
        'patch_wrong_title': '選択されたEBOOT.PBPはCave Storyではありません (タイトル: "{0}")。操作をキャンセルしました。',
        'patch_recognized': 'Cave Storyが正しく認識されました。',
        'patch_csz_not_found': 'data.cszが選択されていません。',
        'patch_io_error': 'EBOOT.PBP読み取りエラー: {0}',
        'patch_error_title': '無効なゲーム',
        'extract_eboot_title': 'EBOOT.PBPを抽出',
        'extract_eboot_select': '抽出するEBOOT.PBPファイルを選択',
        'extract_eboot_start': 'EBOOT.PBPを {0} に抽出中...',
        'extract_eboot_success': 'EBOOT.PBPの抽出が完了しました。',
        'extract_eboot_title_dialog': 'ゲームタイトル: "{0}"\nそれでも抽出しますか？',
        'extract_eboot_warning': 'ゲーム名を変更することをお勧めします。\nその他のパラメータは自己責任で変更してください。',
        'extract_eboot_missing': 'ファイルが抽出されませんでした（空のセクションの可能性があります）。',
        'compress_eboot_title': 'EBOOT.PBPを圧縮',
        'compress_eboot_select_dir': '抽出したEBOOTファイルが含まれるフォルダを選択',
        'compress_eboot_checking': 'フォルダ {0} を確認中...',
        'compress_eboot_missing_data_psp': '選択したフォルダにDATA.PSPが見つかりません。',
        'compress_eboot_missing_pic1': '選択したフォルダにPIC1.PNGが見つかりません。',
        'compress_eboot_success': 'EBOOT.PBPの生成が完了しました。',
        'compress_eboot_saved': '保存先: {0}',
        'compress_eboot_error': '圧縮中にエラーが発生しました: {0}',
        'btn_edit_param': 'PARAM.SFOを編集',
        'edit_param_title': 'PARAM.SFO編集 - ゲームタイトル',
        'edit_param_select_folder': 'PARAM.SFOを含むフォルダを選択',
        'edit_param_not_found': '選択したフォルダにPARAM.SFOが見つかりません。',
        'edit_param_error': 'エラー',
        'edit_param_current': '現在のタイトル:',
        'edit_param_new': '新しいタイトル:',
        'edit_param_warning': 'このファイルを詳細に編集するには、外部プログラムを使用してください。これは名前を簡単に変更するためのものです。',
        'edit_param_long_warning': '名前が長すぎるとクラッシュや予期しないエラーが発生する可能性があります。自己責任で続行してください。',
        'edit_param_empty': 'タイトルを空にできません。',
        'edit_param_too_long': '新しいタイトルがPARAM.SFOの予約スペースを超えています。外部エディタを使用してください。',
        'edit_param_success': 'タイトルを更新しました。',
        'edit_param_save': '保存',
        'btn_restore_eboot': '元のEBOOT.PBPを復元',
        'restore_eboot_title': '元のEBOOT.PBPを復元',
        'restore_eboot_select_zip': '元のEBOOT.PBPを含むZIPファイルを選択',
        'restore_eboot_checking': '{0} からEBOOT.PBPを復元中...',
        'restore_eboot_success': 'EBOOT.PBPの復元が完了しました。',
        'restore_eboot_crc_match': 'CRC32がオリジナルと一致します。',
        'restore_eboot_crc_mismatch': 'CRC32がオリジナルと一致しません。ファイルは変更されている可能性があります。',
        'restore_eboot_no_csz': 'ZIP内にEBOOT.PBPが見つかりません。',
        'restore_eboot_error': '復元中にエラーが発生しました: {0}',
    }
}

# ------------------------------------------------------------
# Detección automática del idioma del sistema
# ------------------------------------------------------------
def detect_system_language():
    try:
        sys_lang, _ = locale.getdefaultlocale()
        if sys_lang is None:
            sys_lang = 'en_US'
        lang_code = sys_lang[:2].lower()
        if lang_code == 'en':
            return 'en'
        elif lang_code == 'es':
            return 'es'
        elif lang_code == 'ja':
            return 'jp'
        else:
            return 'en'
    except:
        return 'en'

current_lang = detect_system_language()

def tr(key, *args):
    text = LANGUAGES[current_lang].get(key, LANGUAGES['en'].get(key, key))
    if args:
        return text.format(*args)
    return text

# ------------------------------------------------------------
# Constantes y funciones comunes para data.csz
# ------------------------------------------------------------
FILENAME_LEN = 64
BLOCKSIZE = 128
VERSION = 0x10001000
FLAG_LOCALIZED = 1 << 0
FLAG_TSC = 1 << 1
EXPECTED_CRC = 0x10BE181C
EXPECTED_EBOOT_CRC = 0x8A97D269

HEADER_FORMAT = "<4sIII"
ENTRY_FORMAT = f"<{FILENAME_LEN}sIIIIIIII"

def calc_crc32(data):
    return zlib.crc32(data) & 0xffffffff

def round_up(value, block=BLOCKSIZE):
    rem = value % block
    return value if rem == 0 else value + block - rem

def detect_locale_and_stripped_name(filename):
    base, ext = os.path.splitext(filename)
    match = re.search(r'\(([12])\)$', base)
    if match:
        locale = int(match.group(1))
        stripped_base = base[:-3]
        stripped_name = stripped_base + ext
        flags = FLAG_LOCALIZED
        if stripped_name.endswith('.tsc'):
            flags |= FLAG_TSC
        return stripped_name, locale, flags
    else:
        flags = 0
        if filename.endswith('.tsc'):
            flags |= FLAG_TSC
        return filename, 0, flags

def collect_files(root_dir):
    file_list = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.startswith('.lang_'):
                continue
            if fname.startswith('.'):
                continue
            full_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
            stored_name = os.path.join("data", rel_path).replace("\\", "/")
            stripped_stored_name, locale, flags = detect_locale_and_stripped_name(stored_name)
            file_list.append((stripped_stored_name, full_path, locale, flags))
    file_list.sort(key=lambda x: x[0])
    return file_list

def build_archive(input_dir, output_archive, log_entries, progress_callback=None):
    file_list = collect_files(input_dir)
    if not file_list:
        return False, tr('err_no_files')
    entries = []
    total_data_size = sum(os.path.getsize(full_path) for _, full_path, _, _ in file_list)
    processed = 0
    for stored_name, full_path, locale, flags in file_list:
        with open(full_path, 'rb') as f:
            content = f.read()
        size = len(content)
        namehash = calc_crc32(stored_name.encode('utf-8'))
        checksum = calc_crc32(content)
        entries.append({
            'filename': stored_name,
            'size': size,
            'namehash': namehash,
            'checksum': checksum,
            'flags': flags,
            'locale': locale,
            'content': content,
        })
        processed += size
        if progress_callback:
            progress_callback(processed, total_data_size)
    header_size = struct.calcsize("<4sIII") + len(entries) * struct.calcsize(f"<{FILENAME_LEN}sIIIIIIII")
    first_offset = round_up(header_size)
    offset = first_offset
    for e in entries:
        e['offset'] = offset
        offset = round_up(offset + e['size'])
    total_size = offset
    with open(output_archive, 'wb') as f:
        f.write(struct.pack("<4sIII", b'Cave', VERSION, total_size, len(entries)))
        for e in entries:
            fn = e['filename'].encode('utf-8')[:FILENAME_LEN].ljust(FILENAME_LEN, b'\x00')
            f.write(struct.pack(f"<{FILENAME_LEN}sIIIIIIII",
                                fn, e['size'], e['offset'], e['namehash'],
                                e['checksum'], e['flags'], e['locale'], 0, 0))
        pad = first_offset - header_size
        if pad > 0:
            f.write(b'\x00' * pad)
        dummy = b'\x00' * BLOCKSIZE
        for e in entries:
            f.write(e['content'])
            to_pad = round_up(e['size']) - e['size']
            if to_pad:
                f.write(dummy[:to_pad])
    log_entries.extend(entries)
    return True, tr('log_compress_ok', total_size, len(entries))

def compress_archive(archive_file, output_csz):
    with open(archive_file, 'rb') as f:
        raw = f.read()
    unc_len = len(raw)
    comp = zlib.compress(raw, level=9)
    with open(output_csz, 'wb') as f:
        f.write(struct.pack('<I', unc_len))
        f.write(comp)
    return tr('log_compress_compressed', unc_len, len(comp))

def write_log(log_entries, log_file="archive.dat"):
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("List of files packed into data.csz\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'Stored name':<64} {'Size':>10} {'Locale':>6} {'Flags':>6} {'Offset':>8}\n")
        f.write("-" * 100 + "\n")
        for e in log_entries:
            f.write(f"{e['filename']:<64} {e['size']:>10} {e['locale']:>6} {e['flags']:>6} {e['offset']:>8}\n")

def decompress_archive(csz_file, output_dir, filter_locale=None, add_suffix=False, progress_callback=None):
    with open(csz_file, 'rb') as f:
        compressed = f.read()
    if len(compressed) < 4:
        return False, tr('err_small')
    unc_size = struct.unpack('<I', compressed[:4])[0]
    try:
        archive = zlib.decompress(compressed[4:])
    except zlib.error as e:
        return False, tr('err_decompress', str(e))
    if len(archive) < struct.calcsize(HEADER_FORMAT):
        return False, tr('err_incomplete')
    header = struct.unpack(HEADER_FORMAT, archive[:struct.calcsize(HEADER_FORMAT)])
    version, total_size, num_files = header[1], header[2], header[3]
    entry_size = struct.calcsize(ENTRY_FORMAT)
    base = struct.calcsize(HEADER_FORMAT)
    files_to_extract = []
    total_extract_size = 0
    for i in range(num_files):
        off = base + i * entry_size
        data = archive[off:off+entry_size]
        unpacked = struct.unpack(ENTRY_FORMAT, data)
        stored_name = unpacked[0].split(b'\x00', 1)[0].decode('utf-8', errors='replace')
        size = unpacked[1]
        offset = unpacked[2]
        locale = unpacked[6]
        if filter_locale is not None and locale != filter_locale and locale != 0:
            continue
        rel = stored_name
        if rel.startswith("data/"):
            rel = rel[5:]
        elif rel.startswith("data\\"):
            rel = rel[5:]
        if add_suffix and locale == 1:
            base_name, ext = os.path.splitext(rel)
            rel = f"{base_name}(1){ext}"
        elif add_suffix and locale == 2:
            base_name, ext = os.path.splitext(rel)
            rel = f"{base_name}(2){ext}"
        files_to_extract.append((rel, offset, size))
        total_extract_size += size
    if not files_to_extract:
        if filter_locale == 1:
            return False, tr('err_no_english')
        elif filter_locale == 2:
            return False, tr('err_no_japanese')
        else:
            return False, "No files found in archive."
    os.makedirs(output_dir, exist_ok=True)
    extracted = 0
    processed = 0
    for rel, offset, size in files_to_extract:
        out_path = os.path.join(output_dir, rel)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        file_data = archive[offset:offset+size]
        with open(out_path, 'wb') as f:
            f.write(file_data)
        extracted += 1
        processed += size
        if progress_callback:
            progress_callback(processed, total_extract_size)
    return True, f"Extracted {extracted} files to '{output_dir}'"

def restore_from_zip(zip_path, progress_callback=None):
    if not os.path.isfile(zip_path):
        return False, tr('err_no_zip')
    temp_dir = "restore_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            members = zf.infolist()
            total_size = sum(m.file_size for m in members)
            extracted_size = 0
            for member in members:
                zf.extract(member, temp_dir)
                extracted_size += member.file_size
                if progress_callback:
                    progress_callback(extracted_size, total_size)
    except Exception as e:
        shutil.rmtree(temp_dir)
        return False, f"Error extracting ZIP: {e}"
    csz_files = []
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.lower().endswith('.csz'):
                csz_files.append(os.path.join(root, file))
    if not csz_files:
        shutil.rmtree(temp_dir)
        return False, "No .csz file found inside ZIP"
    origen = csz_files[0]
    destino = "data.csz"
    shutil.copy2(origen, destino)
    original_date = (2007, 7, 8, 16, 53, 56, 0, 0, 0)
    timestamp = time.mktime(original_date)
    os.utime(destino, (timestamp, timestamp))
    crc = calc_crc32(open(destino, 'rb').read())
    msg = tr('log_restore_crc', destino, crc)
    ok = (crc == EXPECTED_CRC)
    shutil.rmtree(temp_dir)
    if not ok:
        msg += "\n" + tr('log_restore_warn')
    return ok, msg

# ------------------------------------------------------------
# Funciones para EBOOT.PBP y PARAM.SFO
# ------------------------------------------------------------
PBP_SECTIONS = [
    "PARAM.SFO",
    "ICON0.PNG",
    "ICON1.PMF",
    "PIC0.PNG",
    "PIC1.PNG",
    "SND0.AT3",
    "DATA.PSP",
    "UNK"
]

def read_eboot_sections(eboot_path):
    with open(eboot_path, 'rb') as f:
        header = f.read(8)
        if len(header) < 8 or header[:4] != b'\x00PBP':
            raise ValueError("Not a valid PSP EBOOT.PBP file")
        f.seek(8)
        offsets = struct.unpack('<8I', f.read(32))
        sections = []
        for i, section_name in enumerate(PBP_SECTIONS):
            if i >= len(offsets):
                break
            offset = offsets[i]
            next_offset = offsets[i+1] if i+1 < len(offsets) else os.path.getsize(eboot_path)
            if offset > 0 and offset < next_offset:
                f.seek(offset)
                data = f.read(next_offset - offset)
            else:
                data = b''
            sections.append((section_name, data))
        if len(offsets) > len(PBP_SECTIONS) and offsets[-1] > 0:
            f.seek(offsets[-1])
            data = f.read()
            sections.append(("EXTRA", data))
        return sections

def write_eboot_from_sections(sections, output_path):
    full_sections = []
    for i in range(8):
        if i < len(sections):
            full_sections.append(sections[i][1])
        else:
            full_sections.append(b'')
    file_size = 8 + 32
    offsets = []
    for data in full_sections:
        offsets.append(file_size)
        file_size += len(data)
    with open(output_path, 'wb') as f:
        f.write(b'\x00PBP\x00\x00\x00\x00')
        f.write(struct.pack('<8I', *offsets))
        for data in full_sections:
            f.write(data)

def parse_sfo(data):
    """Analiza un PARAM.SFO y devuelve (dict_campos, info_estructura) para edición."""
    if len(data) < 20 or data[:4] != b'\x00PSF':
        return None, None
    # Leer cabecera (20 bytes)
    version, key_start, data_start, num_items = struct.unpack('<IIII', data[4:20])
    # Validar rangos (si valores parecen inválidos, intentar cabecera de 16 bytes)
    if key_start >= len(data) or data_start >= len(data) or num_items > 200:
        # Intentar cabecera de 16 bytes (formato antiguo)
        key_start, data_start, num_items = struct.unpack('<HHH', data[8:14])
        header_size = 16
    else:
        header_size = 20
    # Leer índices
    entries = []
    pos = header_size
    for i in range(num_items):
        if pos + 16 > len(data):
            break
        entry = data[pos:pos+16]
        key_off, data_fmt, data_len, data_max, data_off = struct.unpack('<HHIII', entry)
        # Leer clave
        key_end = data.find(b'\x00', key_start + key_off)
        if key_end == -1:
            key_end = len(data)
        key = data[key_start+key_off:key_end].decode('utf-8', errors='ignore')
        # Leer valor
        val_start = data_start + data_off
        if data_fmt == 0x0204:  # string
            raw = data[val_start:val_start+data_len]
            val = raw.split(b'\x00')[0].decode('utf-8', errors='ignore')
        elif data_fmt == 0x0404:  # integer
            val = struct.unpack('<I', data[val_start:val_start+4])[0] if data_len >= 4 else 0
        else:
            val = data[val_start:val_start+data_len]
        # Guardar junto con offsets para poder modificar después
        entries.append({
            'key': key,
            'value': val,
            'key_off': key_off,
            'data_off': data_off,
            'data_len': data_len,
            'data_fmt': data_fmt
        })
        pos += 16
    # Crear diccionario para acceso rápido
    result = {e['key']: e['value'] for e in entries}
    return result, {'entries': entries, 'key_start': key_start, 'data_start': data_start, 'header_size': header_size}

def get_param_sfo_title(param_sfo_data):
    parsed, _ = parse_sfo(param_sfo_data)
    if parsed is None:
        return None
    return parsed.get('TITLE')

def extract_eboot(eboot_path, output_dir):
    sections = read_eboot_sections(eboot_path)
    os.makedirs(output_dir, exist_ok=True)
    count = 0
    for name, data in sections:
        if data:
            file_path = os.path.join(output_dir, name)
            with open(file_path, 'wb') as f:
                f.write(data)
            count += 1
    param_data = next((data for name, data in sections if name == "PARAM.SFO"), None)
    return count, param_data

def compress_eboot(input_dir, output_eboot):
    data_psp = os.path.join(input_dir, "DATA.PSP")
    pic1 = os.path.join(input_dir, "PIC1.PNG")
    if not os.path.isfile(data_psp):
        return False, tr('compress_eboot_missing_data_psp')
    if not os.path.isfile(pic1):
        return False, tr('compress_eboot_missing_pic1')
    section_files = ["PARAM.SFO", "ICON0.PNG", "ICON1.PMF", "PIC0.PNG", "PIC1.PNG", "SND0.AT3", "DATA.PSP"]
    sections = []
    for fname in section_files:
        path = os.path.join(input_dir, fname)
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                data = f.read()
        else:
            data = b''
        sections.append((fname, data))
    write_eboot_from_sections(sections, output_eboot)
    return True, tr('compress_eboot_success')

# ------------------------------------------------------------
# Clase principal de la interfaz
# ------------------------------------------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.lang_var = StringVar(value=current_lang)
        root.title(tr('app_title'))
        root.geometry("720x620")  # Ventana más pequeña
        root.minsize(640, 620)

        top_frame = Frame(root, bg="#2c3e50", pady=6)
        top_frame.pack(fill=X)

        credit_container = Frame(top_frame, bg="#2c3e50")
        credit_container.pack(side=LEFT, expand=True, fill=BOTH)
        self.credit_label = Label(credit_container, text=tr('credit'), fg="white", bg="#2c3e50",
                                  font=("Courier new", 8, "bold"), justify=CENTER)
        self.credit_label.pack(expand=True)

        lang_frame = Frame(top_frame, bg="#2c3e50")
        lang_frame.pack(side=RIGHT, padx=5, pady=5)
        Label(lang_frame, text="🌐", bg="#2c3e50", fg="white").pack(side=RIGHT)
        self.lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                                       values=[LANGUAGES[k]['name'] for k in LANGUAGES],
                                       state="readonly", width=14)
        self.lang_combo.pack(side=RIGHT)
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)

        self.btn_help = Button(top_frame, text="?", command=self.open_help, font=("Courier new", 10, "bold"),
                               bg="#f39c12", fg="white", width=3, relief=FLAT)
        self.btn_help.pack(side=RIGHT, padx=(0, 10), pady=5)

        button_frame = Frame(root, pady=8)
        button_frame.pack()

        colors = {
            "full": {"bg": "#3498db", "fg": "white", "active": "#2980b9"},
            "en": {"bg": "#2ecc71", "fg": "white", "active": "#27ae60"},
            "jp": {"bg": "#e67e22", "fg": "white", "active": "#d35400"},
            "compress": {"bg": "#9b59b6", "fg": "white", "active": "#8e44ad"},
            "restore": {"bg": "#e74c3c", "fg": "white", "active": "#c0392b"},
            "patch": {"bg": "#1abc9c", "fg": "white", "active": "#16a085"},
            "extract_eboot": {"bg": "#f1c40f", "fg": "black", "active": "#f39c12"},
            "compress_eboot": {"bg": "#e84393", "fg": "white", "active": "#c44569"},
            "edit_param": {"bg": "#95a5a6", "fg": "white", "active": "#7f8c8d"},
            "restore_eboot": {"bg": "#2c3e50", "fg": "white", "active": "#1a252f"}
        }

        # Botones con espaciado reducido
        self.btn_full = Button(button_frame, text=tr('btn_full'), command=self.decompress_all, width=48,
                               bg=colors["full"]["bg"], fg=colors["full"]["fg"],
                               activebackground=colors["full"]["active"])
        self.btn_full.pack(pady=2)

        self.btn_en = Button(button_frame, text=tr('btn_en'), command=self.decompress_english, width=48,
                             bg=colors["en"]["bg"], fg=colors["en"]["fg"],
                             activebackground=colors["en"]["active"])
        self.btn_en.pack(pady=2)

        self.btn_jp = Button(button_frame, text=tr('btn_jp'), command=self.decompress_japanese, width=48,
                             bg=colors["jp"]["bg"], fg=colors["jp"]["fg"],
                             activebackground=colors["jp"]["active"])
        self.btn_jp.pack(pady=2)

        self.btn_compress = Button(button_frame, text=tr('btn_compress'), command=self.compress, width=48,
                                   bg=colors["compress"]["bg"], fg=colors["compress"]["fg"],
                                   activebackground=colors["compress"]["active"])
        self.btn_compress.pack(pady=2)

        self.btn_restore = Button(button_frame, text=tr('btn_restore'), command=self.restore, width=48,
                                  bg=colors["restore"]["bg"], fg=colors["restore"]["fg"],
                                  activebackground=colors["restore"]["active"])
        self.btn_restore.pack(pady=2)

        self.btn_patch = Button(button_frame, text=tr('btn_patch'), command=self.patch_eboot, width=48,
                                bg=colors["patch"]["bg"], fg=colors["patch"]["fg"],
                                activebackground=colors["patch"]["active"])
        self.btn_patch.pack(pady=2)

        self.btn_extract_eboot = Button(button_frame, text=tr('btn_extract_eboot'), command=self.extract_eboot_gui, width=48,
                                        bg=colors["extract_eboot"]["bg"], fg=colors["extract_eboot"]["fg"],
                                        activebackground=colors["extract_eboot"]["active"])
        self.btn_extract_eboot.pack(pady=2)

        self.btn_compress_eboot = Button(button_frame, text=tr('btn_compress_eboot'), command=self.compress_eboot_gui, width=48,
                                         bg=colors["compress_eboot"]["bg"], fg=colors["compress_eboot"]["fg"],
                                         activebackground=colors["compress_eboot"]["active"])
        self.btn_compress_eboot.pack(pady=2)

        self.btn_edit_param = Button(button_frame, text=tr('btn_edit_param'), command=self.edit_param_sfo, width=48,
                                     bg=colors["edit_param"]["bg"], fg=colors["edit_param"]["fg"],
                                     activebackground=colors["edit_param"]["active"])
        self.btn_edit_param.pack(pady=2)

        self.btn_restore_eboot = Button(button_frame, text=tr('btn_restore_eboot'), command=self.restore_eboot_original, width=48,
                                        bg=colors["restore_eboot"]["bg"], fg=colors["restore_eboot"]["fg"],
                                        activebackground=colors["restore_eboot"]["active"])
        self.btn_restore_eboot.pack(pady=2)

        self.progress_frame = Frame(root)
        self.progress_frame.pack(pady=5, fill=X, padx=10)
        self.progress_label = Label(self.progress_frame, text="")
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=HORIZONTAL, length=400, mode='determinate')
        self.progress_bar.pack(pady=2)

        log_frame = Frame(root)
        log_frame.pack(padx=10, pady=5, fill=BOTH, expand=True)

        log_buttons_frame = Frame(log_frame)
        log_buttons_frame.pack(fill=X, pady=2)
        self.btn_copy = Button(log_buttons_frame, text=tr('btn_copy_log'), command=self.copy_log, width=12)
        self.btn_copy.pack(side=LEFT, padx=2)
        self.btn_clear = Button(log_buttons_frame, text=tr('btn_clear_log'), command=self.clear_log, width=12)
        self.btn_clear.pack(side=LEFT, padx=2)

        # Área de log con altura reducida
        self.log = scrolledtext.ScrolledText(log_frame, wrap=WORD, height=8, width=75, state='disabled')
        self.log.pack(fill=BOTH, expand=True)

        sys.stdout = TextRedirector(self.log)

    def update_texts(self):
        self.root.title(tr('app_title'))
        self.credit_label.config(text=tr('credit'))
        self.btn_full.config(text=tr('btn_full'))
        self.btn_en.config(text=tr('btn_en'))
        self.btn_jp.config(text=tr('btn_jp'))
        self.btn_compress.config(text=tr('btn_compress'))
        self.btn_restore.config(text=tr('btn_restore'))
        self.btn_patch.config(text=tr('btn_patch'))
        self.btn_extract_eboot.config(text=tr('btn_extract_eboot'))
        self.btn_compress_eboot.config(text=tr('btn_compress_eboot'))
        self.btn_edit_param.config(text=tr('btn_edit_param'))
        self.btn_restore_eboot.config(text=tr('btn_restore_eboot'))
        self.btn_copy.config(text=tr('btn_copy_log'))
        self.btn_clear.config(text=tr('btn_clear_log'))

    def change_language(self, event=None):
        global current_lang
        selected = self.lang_combo.get()
        for k, v in LANGUAGES.items():
            if v['name'] == selected:
                current_lang = k
                break
        self.update_texts()

    def log_message(self, msg):
        self.log.config(state='normal')
        self.log.insert(END, msg + "\n")
        self.log.see(END)
        self.log.config(state='disabled')
        self.root.update_idletasks()

    def copy_log(self):
        self.log.config(state='normal')
        content = self.log.get(1.0, END)
        self.log.config(state='disabled')
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.log_message(tr('log_copied'))

    def clear_log(self):
        self.log.config(state='normal')
        self.log.delete(1.0, END)
        self.log.config(state='disabled')
        self.log_message(tr('log_cleared'))

    def open_help(self):
        help_win = Toplevel(self.root)
        help_win.title(tr('help_title'))
        help_win.geometry("550x500")
        help_win.minsize(450, 400)
        help_win.transient(self.root)
        help_win.grab_set()

        # Contenido según idioma
        if current_lang == 'es':
            help_content = """-- ¿Que Hace Esta Herramienta? --

Esta herramienta permite:
- Extraer y modificar data.csz (archivos de datos del juego)
- Aplicar parches al juego (reemplazar data.csz)
- Extraer y reconstruir EBOOT.PBP (secciones individuales)
- Editar rápidamente el título del juego en PARAM.SFO
- Restaurar el EBOOT.PBP original desde un ZIP
- Extraer el contenido de un PBP

-- FUNCIONES --

DESCOMPRIMIR .csz (1)(2)
Al descomprimir se creará una carpeta data, los archivos con un (1) son inglés y (2) japonés.

DESCOMPRIMIR .csz inglés
Solo se descomprimirán los archivos en inglés sin sus subfijos (1), modifica su contenido o mueve la carpeta data de tu mod freeware a esta.

DESCOMPRIMIR .csz japonés
Solo se descomprimirán los archivos en japonés sin sus subfijos (2), modifica su contenido o mueve la carpeta data de tu mod freeware a esta.

COMPRIMIR .csz
Comprime la carpeta data extraida devuelta a data.csz.

RESTAURAR .csz Original
Restaura el .csz original desde un zip, eso si, si modificaste el data.csz actual, el original reemplazará el modificado.

APLICAR PARCHE
Selecciona el data.csz sin modificar, el csz modificado se aplicará al no modificado.

EXTRAER EBOOT.PBP
Extrae el contenido del EBOOT.PBP para que puedas editar su contenido.

COMRIMIR EBOOT.PBP
La carpeta del EBOOT extraido se comprimirá devuelta como EBOOT.PBP

EDITAR PARAM.SFO
Edita el nombre del juego y se aplica al PARAM.SFO extraido

RESTAURAR EBOOT.PBP Original
Restaura el .PBP original desde un zip, eso si, si modificaste el .PBP actual, el original reemplazará el modificado.

-- Preguntas Y Respuestas --

1. ¿Para qué sirve esta herramienta?
   Permite extraer y modificar los archivos data.csz y EBOOT.PBP del juego Cave Story para PSP, así como aplicar parches y modificar el título del juego.

2. ¿Cómo extraigo los archivos del juego?
   Use los botones "Extraer Completo" (para ambos idiomas con sufijos (1)/(2)), "Extraer Inglés" o "Extraer Japonés". Se creará una carpeta "data" con los archivos.

3. ¿Cómo vuelvo a empaquetar los archivos?
   Después de modificar los archivos en la carpeta "data", presione "Comprimir". Se generará un nuevo data.csz.

4. ¿Qué hago si el juego no arranca después de modificar?
   Asegúrese de haber extraído el idioma correcto (inglés o japonés) y no mezclar archivos. Si usa "Extraer Completo", el data.csz resultante contendrá ambos idiomas.

5. ¿Cómo aplico un parche (mod) al juego?
   Use "Apply Patch/Mod to Cave Story PSP". Seleccione el EBOOT.PBP (si ya está en la carpeta se seleccionará solo),
   luego el data.csz modificado (si ya está en la carpeta se seleccionará solo) luego el data.csz original. El programa reemplazará el data.csz original
   en la carpeta del EBOOT de tu juego.

6. ¿Por qué aparece el error "El proceso no tiene acceso al archivo"?
   Asegúrese de que no tenga abierto el juego, el emulador PPSSPP, el explorador de archivos con vista previa, o el antivirus.
   No intente parchear con el mismo archivo data.csz (seleccione uno diferente).

7. ¿Cómo edito el nombre del juego que aparece en la PSP?
   Extraiga el EBOOT.PBP (botón "Extraer EBOOT.PBP"), luego use "Editar PARAM.SFO" para cambiar el título. Luego recomponga el EBOOT con "Comprimir EBOOT.PBP".

8. ¿Puedo restaurar el EBOOT original?
   Sí, con "Restaurar EBOOT.PBP Original". Necesita un archivo ZIP llamado "original_eboot.zip" (o seleccionar uno manualmente) que contenga el EBOOT original.

9. ¿Los archivos extraídos conservan los sufijos (1) y (2)?
   Solo "Extraer Completo" añade los sufijos. "Extraer Inglés" y "Extraer Japonés" no añaden sufijos para facilitar la edición directa.

10. ¿La herramienta modifica los archivos originales?
    No modifica el data.csz original a menos que usted lo sobrescriba al comprimir o parchear. Se recomienda hacer copias de seguridad.

   ¿Y si mi pregunta no está aqui?
   Haz preguntas en el thread o envia un issue en Github

Créditos:
- Codigo de las herramientas csz originales por andwhyisit
- Porteado a Python por EdwarlyGamer999+
- Cave Story PSP by ufo_z

THREAD: https://forum.cavestory.one/threads/csz-tools.18220/
GITHUB: https://github.com/edwarly999plus/CSZ-Tools-Plus
"""
        elif current_lang == 'jp':
            help_content = """-- このツールの機能 --

このツールを使用すると次のことができます：
- data.csz（ゲームデータファイル）の抽出・変更
- ゲームへのパッチ適用（data.cszの置き換え）
- EBOOT.PBPの抽出と再構築（個別セクション）
- PARAM.SFOでゲームタイトルを素早く編集
- ZIPから元のEBOOT.PBPを復元
- PBPの内容を抽出

-- 機能 --

EXTRACT ALL .csz (1)(2)
抽出すると「data」フォルダが作成されます。(1)の付いたファイルは英語版、(2)は日本語版です。

EXTRACT ENGLISH .csz
サフィックス(1)なしで英語ファイルのみ抽出します。内容を編集したり、Freeware版MODのdataフォルダをこちらに移動できます。

EXTRACT JAPANESE .csz
サフィックス(2)なしで日本語ファイルのみ抽出します。内容を編集したり、Freeware版MODのdataフォルダをこちらに移動できます。

COMPRESS .csz
抽出したdataフォルダをdata.cszに圧縮し戻します。

RESTORE ORIGINAL .csz
ZIPから元の.cszを復元します。現在のdata.cszを変更した場合、元のファイルで上書きされます。

APPLY PATCH
変更するdata.cszを選択し、元のdata.cszに適用します（EBOOTフォルダ内のdata.cszを置き換えます）。

EXTRACT EBOOT.PBP
EBOOT.PBPの内容を抽出し編集できるようにします。

COMPRESS EBOOT.PBP
抽出したEBOOTフォルダを再びEBOOT.PBPに圧縮します。

EDIT PARAM.SFO
ゲームのタイトルを編集し、抽出済みのPARAM.SFOに適用します。

RESTORE ORIGINAL EBOOT.PBP
ZIPから元の.PBPを復元します。現在の.PBPを変更した場合、元のファイルで上書きされます。

-- よくある質問（FAQ） --

1. このツールの目的は何ですか？
   Cave Story PSPのdata.cszとEBOOT.PBPファイルを抽出、変更、パッチ適用、ゲームタイトルの編集を行うことができます。

2. ゲームファイルを抽出するには？
   「すべて抽出」（両言語、サフィックス(1)/(2)付き）、「英語抽出」、「日本語抽出」ボタンを使用します。「data」フォルダが作成されます。

3. ファイルを再パックするには？
   「data」フォルダ内のファイルを修正した後、「圧縮」を押します。新しいdata.cszが生成されます。

4. 変更後、ゲームが起動しない場合は？
   正しい言語（英語または日本語）を抽出し、ファイルを混在させていないか確認してください。「すべて抽出」を使用すると、両方の言語が含まれます。

5. パッチ（Mod）を適用するには？
   「Apply Patch/Mod to Cave Story PSP」を使用します。EBOOT.PBP（カレントフォルダにあれば自動選択）、次に変更したdata.csz（同じく自動選択）、最後に元のdata.cszを選択します。プログラムはEBOOTフォルダ内のdata.cszを置き換えます。

6. 「プロセスがファイルにアクセスできません」というエラーが表示されるのはなぜですか？
   ゲーム、PPSSPPエミュレーター、プレビュー付きのファイルエクスプローラー、アンチウイルスが開いていないことを確認してください。
   同じdata.cszファイルでパッチを適用しようとしないでください（別のファイルを選択してください）。

7. PSPに表示されるゲーム名を編集するには？
   EBOOT.PBPを抽出（「EBOOT.PBPを抽出」ボタン）し、「PARAM.SFOを編集」でタイトルを変更します。その後、「EBOOT.PBPを圧縮」で再構築します。

8. 元のEBOOTを復元できますか？
   はい、「元のEBOOT.PBPを復元」で可能です。「original_eboot.zip」というZIPファイル（または手動で選択）に元のEBOOTが含まれている必要があります。

9. 抽出されたファイルにサフィックス(1)(2)は付きますか？
   「すべて抽出」のみサフィックスを追加します。「英語抽出」と「日本語抽出」はサフィックスを追加せず、直接編集しやすくなっています。

10. このツールは元のファイルを変更しますか？
    圧縮またはパッチを適用して上書きしない限り、元のdata.cszは変更されません。バックアップを取ることをお勧めします。

    質問がここにない場合は？
    フォーラムスレッドで質問するか、GitHubでIssueを送ってください。

クレジット:
- オリジナルcszツールのコード by andwhyisit
- Python移植 by EdwarlyGamer999+
- Cave Story PSP by ufo_z

THREAD: https://forum.cavestory.one/threads/csz-tools.18220/
GITHUB: https://github.com/edwarly999plus/CSZ-Tools-Plus
"""
        else:  # English by default
            help_content = """-- What Does This Tool Do? --

This tool allows you to:
- Extract and modify data.csz (game data files)
- Apply patches to the game (replace data.csz)
- Extract and rebuild EBOOT.PBP (individual sections)
- Quickly edit the game title in PARAM.SFO
- Restore the original EBOOT.PBP from a ZIP
- Extract the contents of a PBP

-- FUNCTIONS --

EXTRACT ALL .csz (1)(2)
Extracting will create a "data" folder; files with (1) are English, (2) are Japanese.

EXTRACT ENGLISH .csz
Extracts only English files without the (1) suffix. You can modify the content or move the "data" folder from your freeware mod here.

EXTRACT JAPANESE .csz
Extracts only Japanese files without the (2) suffix. You can modify the content or move the "data" folder from your freeware mod here.

COMPRESS .csz
Compresses the extracted data folder back into data.csz.

RESTORE ORIGINAL .csz
Restores the original .csz from a ZIP. Changes you made to the current data.csz will be overwritten.

APPLY PATCH
Select the unmodified data.csz, then select the modified data.csz. The program will replace the original data.csz in the EBOOT folder.

EXTRACT EBOOT.PBP
Extracts the contents of the EBOOT.PBP so you can edit them.

COMPRESS EBOOT.PBP
Compresses the extracted EBOOT folder back into EBOOT.PBP.

EDIT PARAM.SFO
Edits the game name and applies the change to the extracted PARAM.SFO.

RESTORE ORIGINAL EBOOT.PBP
Restores the original .PBP from a ZIP. Changes you made to the current .PBP will be overwritten.

-- FREQUENTLY ASKED QUESTIONS (FAQ) --

1. What is this tool for?
   It allows extracting and modifying data.csz and EBOOT.PBP files of Cave Story for PSP, as well as applying patches and editing the game title.

2. How do I extract the game files?
   Use the buttons "Extract All" (adds suffixes (1)/(2) for both languages), "Extract English" or "Extract Japanese". A "data" folder will be created.

3. How do I repack the files?
   After modifying files in the "data" folder, press "Compress". A new data.csz will be generated.

4. What if the game doesn't start after modifications?
   Make sure you extracted the correct language (English or Japanese) and did not mix files. If you used "Extract All", the resulting data.csz will contain both languages.

5. How do I apply a patch (mod) to the game?
   Use "Apply Patch/Mod to Cave Story PSP". Select the EBOOT.PBP (if already in the folder it will be auto‑selected),
   then the modified data.csz (if already in the folder it will be auto‑selected), then the original data.csz. The program will replace the original data.csz
   in the EBOOT folder of your game.

6. Why do I get the error "The process cannot access the file"?
   Ensure you don't have the game, PPSSPP emulator, File Explorer with preview, or antivirus open.
   Do not try to patch using the same data.csz file (select a different one).

7. How do I edit the game name shown on the PSP?
   Extract the EBOOT.PBP (button "Extract EBOOT.PBP"), then use "Edit PARAM.SFO" to change the title. Then rebuild the EBOOT with "Compress EBOOT.PBP".

8. Can I restore the original EBOOT?
   Yes, with "Restore Original EBOOT.PBP". You need a ZIP file named "original_eboot.zip" (or select one manually) containing the original EBOOT.

9. Do extracted files keep the (1) and (2) suffixes?
   Only "Extract All" adds the suffixes. "Extract English" and "Extract Japanese" do not add suffixes to facilitate direct editing.

10. Does the tool modify the original files?
    It does not modify the original data.csz unless you overwrite it by compressing or patching. It is recommended to make backups.

    What if my question is not here?
    Ask on the forum thread or open an issue on GitHub.

Credits:
- Original csz tools code by andwhyisit
- Python port by EdwarlyGamer999+
- Cave Story PSP by ufo_z

THREAD: https://forum.cavestory.one/threads/csz-tools.18220/
GITHUB: https://github.com/edwarly999plus/CSZ-Tools-Plus
"""
        text_area = scrolledtext.ScrolledText(help_win, wrap=WORD, font=("Courier New", 10))
        text_area.insert(INSERT, help_content)
        text_area.config(state='disabled')
        text_area.pack(fill=BOTH, expand=True, padx=10, pady=10)
        Button(help_win, text=tr('help_close'), command=help_win.destroy).pack(pady=10)

    def update_progress(self, current, total):
        if total <= 0:
            percent = 0
            size_str = "0 KB"
        else:
            percent = int(current * 100 / total)
            size_str = f"{current/1024:.1f} KB / {total/1024:.1f} KB"
        self.progress_label.config(text=f"{size_str} ({percent}%)")
        self.progress_bar['value'] = percent
        self.root.update_idletasks()

    def reset_progress(self):
        self.progress_label.config(text="")
        self.progress_bar['value'] = 0
        self.root.update_idletasks()

    def run_task_with_progress(self, target, *args):
        def task():
            try:
                self.reset_progress()
                result = target(*args)
                if isinstance(result, tuple):
                    success, msg = result
                    if success:
                        self.log_message("[OK] " + msg)
                    else:
                        self.log_message("[ERROR] " + msg)
                else:
                    self.log_message(str(result))
            except Exception as e:
                self.log_message(f"[EXCEPTION] {e}")
            finally:
                self.reset_progress()
        threading.Thread(target=task, daemon=True).start()

    def get_csz_file(self):
        if os.path.isfile("data.csz"):
            return "data.csz"
        else:
            msgbox = messagebox.askyesno(tr('err_no_csz'), tr('ask_manual_csz'))
            if msgbox:
                return filedialog.askopenfilename(title=tr('err_no_csz'), filetypes=[("CSZ files", "*.csz")])
            else:
                return None

    def decompress_all(self):
        csz = self.get_csz_file()
        if not csz:
            return
        if not messagebox.askyesno(tr('confirm_extract_all'), tr('confirm_extract_all_msg')):
            self.log_message(tr('log_cancelled'))
            return
        out_dir = "data"
        for marker in [".lang_en", ".lang_jp", ".lang_both"]:
            marker_path = os.path.join(out_dir, marker)
            if os.path.exists(marker_path):
                os.remove(marker_path)
        self.log_message(tr('log_full_start', csz, out_dir))
        self.run_task_with_progress(self._extract_all_task, csz, out_dir, True)

    def _extract_all_task(self, csz, out_dir, add_suffix):
        success, msg = decompress_archive(csz, out_dir, None, add_suffix, self.update_progress)
        if success:
            with open(os.path.join(out_dir, ".lang_both"), 'w') as f:
                pass
        return success, msg

    def decompress_english(self):
        csz = self.get_csz_file()
        if not csz:
            return
        if not messagebox.askyesno(tr('confirm_extract_english'), tr('confirm_extract_english_msg')):
            self.log_message(tr('log_cancelled'))
            return
        out_dir = "data"
        for marker in [".lang_en", ".lang_jp", ".lang_both"]:
            marker_path = os.path.join(out_dir, marker)
            if os.path.exists(marker_path):
                os.remove(marker_path)
        self.log_message(tr('log_en_start', csz, out_dir))
        self.run_task_with_progress(self._extract_english_task, csz, out_dir)

    def _extract_english_task(self, csz, out_dir):
        success, msg = decompress_archive(csz, out_dir, 1, False, self.update_progress)
        if success:
            with open(os.path.join(out_dir, ".lang_en"), 'w') as f:
                pass
        return success, msg

    def decompress_japanese(self):
        csz = self.get_csz_file()
        if not csz:
            return
        if not messagebox.askyesno(tr('confirm_extract_japanese'), tr('confirm_extract_japanese_msg')):
            self.log_message(tr('log_cancelled'))
            return
        out_dir = "data"
        for marker in [".lang_en", ".lang_jp", ".lang_both"]:
            marker_path = os.path.join(out_dir, marker)
            if os.path.exists(marker_path):
                os.remove(marker_path)
        self.log_message(tr('log_jp_start', csz, out_dir))
        self.run_task_with_progress(self._extract_japanese_task, csz, out_dir)

    def _extract_japanese_task(self, csz, out_dir):
        success, msg = decompress_archive(csz, out_dir, 2, False, self.update_progress)
        if success:
            with open(os.path.join(out_dir, ".lang_jp"), 'w') as f:
                pass
        return success, msg

    def compress(self):
        input_dir = "data"
        if not os.path.isdir(input_dir):
            resp = messagebox.askyesno(tr('err_no_dir', input_dir), tr('ask_manual_dir', input_dir))
            if resp:
                input_dir = filedialog.askdirectory(title=tr('err_no_dir', input_dir))
                if not input_dir:
                    return
            else:
                return
        if not messagebox.askyesno(tr('confirm_compress'), tr('confirm_compress_msg')):
            self.log_message(tr('log_cancelled'))
            return
        archive_tmp = "archive.dat.tmp"
        output_csz = "data.csz"
        log_entries = []
        self.log_message(tr('log_compress_start', input_dir))
        def compress_task():
            self.reset_progress()
            success, msg = build_archive(input_dir, archive_tmp, log_entries, self.update_progress)
            if not success:
                self.log_message(f"Error: {msg}")
                return False
            self.log_message(msg)
            self.log_message(compress_archive(archive_tmp, output_csz))
            os.remove(archive_tmp)
            write_log(log_entries, "archive.dat")
            self.log_message(tr('log_compress_log'))
            # Detectar idioma
            if os.path.exists(os.path.join(input_dir, ".lang_both")):
                detected_lang = 'both'
            elif os.path.exists(os.path.join(input_dir, ".lang_en")):
                detected_lang = 'en'
            elif os.path.exists(os.path.join(input_dir, ".lang_jp")):
                detected_lang = 'jp'
            else:
                has_english = any(e['locale'] == 1 for e in log_entries)
                has_japanese = any(e['locale'] == 2 for e in log_entries)
                if has_english and has_japanese:
                    detected_lang = 'both'
                elif has_english:
                    detected_lang = 'en'
                elif has_japanese:
                    detected_lang = 'jp'
                else:
                    detected_lang = 'neutral'
            size_bytes = os.path.getsize(output_csz)
            size_kb = size_bytes / 1024
            size_mb = size_bytes / (1024*1024)
            size_str = f"{size_bytes} bytes ({size_kb:.2f} KB / {size_mb:.3f} MB)"
            lang_map = {'both': tr('lang_both'), 'en': tr('lang_english'), 'jp': tr('lang_japanese'), 'neutral': tr('lang_neutral')}
            self.log_message(f"{tr('compress_result')} {size_str} - {lang_map[detected_lang]}")
            if messagebox.askyesno(tr('confirm_clean', input_dir), tr('confirm_clean', input_dir)):
                shutil.rmtree(input_dir)
                self.log_message(tr('log_compress_clean', input_dir))
            else:
                self.log_message(tr('log_compress_keep', input_dir))
            return True
        self.run_task_with_progress(compress_task)

    def restore(self):
        if not messagebox.askyesno(tr('confirm_restore'), tr('confirm_restore')):
            self.log_message(tr('log_cancelled'))
            return
        zip_path = "data_original.zip"
        if not os.path.isfile(zip_path):
            resp = messagebox.askyesno(tr('err_no_zip'), tr('ask_manual_zip'))
            if resp:
                zip_path = filedialog.askopenfilename(title=tr('err_no_zip'), filetypes=[("ZIP files", "*.zip")])
                if not zip_path:
                    return
            else:
                return
        self.log_message(tr('log_restore_start', zip_path))
        self.run_task_with_progress(restore_from_zip, zip_path, self.update_progress)

    def patch_eboot(self):
        default_eboot = "EBOOT.PBP"
        if os.path.isfile(default_eboot):
            eboot_path = default_eboot
        else:
            if not messagebox.askyesno(tr('patch_error_title'), "No se encontró EBOOT.PBP en la carpeta actual.\n¿Deseas seleccionar uno manualmente?"):
                self.log_message(tr('log_cancelled'))
                return
            eboot_path = filedialog.askopenfilename(title=tr('patch_select_eboot'), filetypes=[("PSP executable", "EBOOT.PBP"), ("All files", "*.*")])
            if not eboot_path:
                self.log_message(tr('log_cancelled'))
                return
        self.run_task_with_progress(self._verify_and_patch, eboot_path)

    def _verify_and_patch(self, eboot_path):
        try:
            sections = read_eboot_sections(eboot_path)
            param_data = next((data for name, data in sections if name == "PARAM.SFO"), None)
            parsed, _ = parse_sfo(param_data) if param_data else (None, None)
            title = parsed.get('TITLE') if parsed else None
            if title is None:
                return False, tr('patch_io_error', "Cannot read PARAM.SFO")
            if title != "Cave Story":
                self.root.after(0, lambda: messagebox.showerror(tr('patch_error_title'), tr('patch_wrong_title', title)))
                return False, tr('patch_wrong_title', title)
            self.log_message(tr('patch_recognized'))
            csz_path = filedialog.askopenfilename(title=tr('patch_select_csz'), filetypes=[("CSZ files", "*.csz")])
            if not csz_path:
                return False, tr('patch_cancel')
            dest_dir = os.path.dirname(eboot_path)
            dest_path = os.path.join(dest_dir, "data.csz")
            self.log_message(tr('patch_copying', csz_path, dest_path))
            shutil.copy2(csz_path, dest_path)
            return True, tr('patch_success')
        except Exception as e:
            return False, str(e)

    def extract_eboot_gui(self):
        default_eboot = "EBOOT.PBP"
        if os.path.isfile(default_eboot):
            eboot_path = default_eboot
        else:
            if not messagebox.askyesno(tr('extract_eboot_title'), "No se encontró EBOOT.PBP en la carpeta actual.\n¿Deseas seleccionar uno manualmente?"):
                self.log_message(tr('log_cancelled'))
                return
            eboot_path = filedialog.askopenfilename(title=tr('extract_eboot_select'), filetypes=[("PSP executable", "EBOOT.PBP"), ("All files", "*.*")])
            if not eboot_path:
                self.log_message(tr('log_cancelled'))
                return
        try:
            sections = read_eboot_sections(eboot_path)
            param_data = next((data for name, data in sections if name == "PARAM.SFO"), None)
            parsed, _ = parse_sfo(param_data) if param_data else (None, None)
            title = parsed.get('TITLE') if parsed else "Unknown"
            if not messagebox.askyesno(tr('extract_eboot_title'), tr('extract_eboot_title_dialog', title) + "\n\n" + tr('extract_eboot_warning')):
                self.log_message(tr('log_cancelled'))
                return
        except Exception as e:
            self.log_message(f"[ERROR] {e}")
            return
        out_dir = "EBOOT_EXTRACTED"
        if os.path.exists(out_dir):
            if not messagebox.askyesno(tr('extract_eboot_title'), f"La carpeta '{out_dir}' ya existe.\n¿Sobrescribir su contenido?"):
                self.log_message(tr('log_cancelled'))
                return
        self.log_message(tr('extract_eboot_start', out_dir))
        self.run_task_with_progress(self._extract_eboot_task, eboot_path, out_dir)

    def _extract_eboot_task(self, eboot_path, out_dir):
        try:
            count, _ = extract_eboot(eboot_path, out_dir)
            if count == 0:
                return False, tr('extract_eboot_missing')
            return True, tr('extract_eboot_success')
        except Exception as e:
            return False, str(e)

    def compress_eboot_gui(self):
        default_dir = "EBOOT_EXTRACTED"
        if os.path.isdir(default_dir):
            input_dir = default_dir
        else:
            if not messagebox.askyesno(tr('compress_eboot_title'), "No se encontró la carpeta 'EBOOT_EXTRACTED'.\n¿Deseas seleccionar una carpeta manualmente?"):
                self.log_message(tr('log_cancelled'))
                return
            input_dir = filedialog.askdirectory(title=tr('compress_eboot_select_dir'))
            if not input_dir:
                self.log_message(tr('log_cancelled'))
                return
        self.log_message(tr('compress_eboot_checking', input_dir))
        data_psp = os.path.join(input_dir, "DATA.PSP")
        pic1 = os.path.join(input_dir, "PIC1.PNG")
        if not os.path.isfile(data_psp):
            messagebox.showerror(tr('compress_eboot_title'), tr('compress_eboot_missing_data_psp'))
            self.log_message(f"[ERROR] {tr('compress_eboot_missing_data_psp')}")
            return
        if not os.path.isfile(pic1):
            messagebox.showerror(tr('compress_eboot_title'), tr('compress_eboot_missing_pic1'))
            self.log_message(f"[ERROR] {tr('compress_eboot_missing_pic1')}")
            return
        output_eboot = "EBOOT.PBP"
        if os.path.exists(output_eboot):
            if not messagebox.askyesno(tr('compress_eboot_title'), f"El archivo '{output_eboot}' ya existe.\n¿Sobrescribirlo?"):
                self.log_message(tr('log_cancelled'))
                return
        self.run_task_with_progress(self._compress_eboot_task, input_dir, output_eboot)

    def _compress_eboot_task(self, input_dir, output_eboot):
        try:
            ok, msg = compress_eboot(input_dir, output_eboot)
            if ok:
                self.log_message(tr('compress_eboot_saved', output_eboot))
            return ok, msg
        except Exception as e:
            return False, tr('compress_eboot_error', str(e))

    def edit_param_sfo(self):
        default_dir = "EBOOT_EXTRACTED"
        if os.path.isdir(default_dir):
            folder = default_dir
        else:
            if not messagebox.askyesno(tr('edit_param_title'), "No se encontró la carpeta 'EBOOT_EXTRACTED'.\n¿Deseas seleccionar una carpeta manualmente?"):
                self.log_message(tr('log_cancelled'))
                return
            folder = filedialog.askdirectory(title=tr('edit_param_select_folder'))
            if not folder:
                self.log_message(tr('log_cancelled'))
                return
        param_file = os.path.join(folder, "PARAM.SFO")
        if not os.path.isfile(param_file):
            messagebox.showerror(tr('edit_param_error'), tr('edit_param_not_found'))
            self.log_message(f"[ERROR] {tr('edit_param_not_found')}")
            return
        try:
            with open(param_file, 'rb') as f:
                sfo_data = f.read()
            parsed, info = parse_sfo(sfo_data)
            if parsed is None or 'TITLE' not in parsed:
                raise ValueError("Invalid PARAM.SFO or TITLE not found")
            title = parsed['TITLE']
        except Exception as e:
            messagebox.showerror(tr('edit_param_error'), f"Cannot read PARAM.SFO: {e}")
            return
        # Ventana de edición
        edit_win = Toplevel(self.root)
        edit_win.title(tr('edit_param_title'))
        edit_win.geometry("440x320")
        edit_win.transient(self.root)
        edit_win.grab_set()
        Label(edit_win, text=tr('edit_param_current')).pack(pady=5)
        current_label = Label(edit_win, text=title, font=("Courier new", 10, "bold"))
        current_label.pack()
        Label(edit_win, text=tr('edit_param_new')).pack(pady=5)
        entry = Entry(edit_win, width=40)
        entry.pack()
        entry.insert(0, title)
        warn = Label(edit_win, text=tr('edit_param_warning'), fg="red", wraplength=400, justify=LEFT)
        warn.pack(pady=5)
        def save():
            new_title = entry.get().strip()
            if not new_title:
                messagebox.showerror(tr('edit_param_error'), tr('edit_param_empty'))
                return
            orig_len = len(title.encode('utf-8')) + 1
            new_len = len(new_title.encode('utf-8')) + 1
            if new_len > orig_len and not messagebox.askyesno(tr('edit_param_warning'), tr('edit_param_long_warning') + "\n\n" + tr('edit_param_save') + "?"):
                return
            try:
                entry_info = None
                for e in info['entries']:
                    if e['key'] == 'TITLE':
                        entry_info = e
                        break
                if entry_info is None:
                    raise ValueError("TITLE entry not found")
                val_start = info['data_start'] + entry_info['data_off']
                new_value = new_title.encode('utf-8') + b'\x00'
                if len(new_value) < entry_info['data_len']:
                    new_value = new_value.ljust(entry_info['data_len'], b'\x00')
                new_data = sfo_data[:val_start] + new_value + sfo_data[val_start+entry_info['data_len']:]
                with open(param_file, 'wb') as f:
                    f.write(new_data)
                messagebox.showinfo(tr('edit_param_title'), tr('edit_param_success'))
                edit_win.destroy()
                self.log_message(f"PARAM.SFO updated: new title '{new_title}'")
            except Exception as e:
                messagebox.showerror(tr('edit_param_error'), str(e))
        Button(edit_win, text=tr('edit_param_save'), command=save).pack(pady=10)

    def restore_eboot_original(self):
        # Confirmación inicial
        if not messagebox.askyesno(tr('restore_eboot_title'), "¿Restaurar EBOOT.PBP original? Se sobrescribirá el archivo actual."):
            self.log_message(tr('log_cancelled'))
            return
        default_zip = "original_eboot.zip"
        if os.path.isfile(default_zip):
            if not messagebox.askyesno(tr('restore_eboot_title'), f"Se encontró el archivo '{default_zip}'.\n¿Restaurar el EBOOT original desde él?"):
                self.log_message(tr('log_cancelled'))
                return
            zip_path = default_zip
        else:
            if not messagebox.askyesno(tr('restore_eboot_title'), "No se encontró 'original_eboot.zip'.\n¿Deseas seleccionar un ZIP manualmente?"):
                self.log_message(tr('log_cancelled'))
                return
            zip_path = filedialog.askopenfilename(title=tr('restore_eboot_select_zip'), filetypes=[("ZIP files", "*.zip")])
            if not zip_path:
                self.log_message(tr('log_cancelled'))
                return
        self.log_message(tr('restore_eboot_checking', zip_path))
        self.run_task_with_progress(self._restore_eboot_task, zip_path)

    def _restore_eboot_task(self, zip_path):
        temp_dir = "restore_eboot_temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                members = zf.namelist()
                eboot_member = None
                for name in members:
                    if name.lower().endswith('.pbp') or name == 'EBOOT.PBP':
                        eboot_member = name
                        break
                if eboot_member is None:
                    return False, tr('restore_eboot_no_csz')
                extracted_path = zf.extract(eboot_member, temp_dir)
                crc = calc_crc32(open(extracted_path, 'rb').read())
                self.log_message(f"CRC32 of extracted EBOOT.PBP: 0x{crc:08X}")
                if crc != EXPECTED_EBOOT_CRC:
                    self.log_message(tr('restore_eboot_crc_mismatch'))
                else:
                    self.log_message(tr('restore_eboot_crc_match'))
                dest_path = "EBOOT.PBP"
                shutil.copy2(extracted_path, dest_path)
                # Forzar fecha original del EBOOT (2007-07-08 16:53:56)
                original_date = (2007, 7, 8, 16, 53, 56, 0, 0, 0)
                timestamp = time.mktime(original_date)
                os.utime(dest_path, (timestamp, timestamp))
                self.log_message(tr('restore_eboot_success'))
                return True, tr('restore_eboot_success')
        except Exception as e:
            return False, tr('restore_eboot_error', str(e))
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, msg):
        self.widget.config(state='normal')
        self.widget.insert(END, msg)
        self.widget.see(END)
        self.widget.config(state='disabled')
    def flush(self):
        pass

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
