;;; package --- summary
;;; Commentary:
;;; Code:
(defvar *emacs-load-start* (current-time))

(add-to-list 'load-path "/home/gabe/emacs/")
(add-to-list 'load-path "/home/gabe/emacs/yaml-mode/")
(add-to-list 'load-path "/home/gabe/emacs/typescript-mode/")
(add-to-list 'load-path "/home/gabe/emacs/markdown-mode/")

;; (autoload 'ledger-mode "ledger-mode" "A major mode for Ledger" t)
(add-to-list 'load-path  "/home/gabe/emacs/ledger-mode/")
(require 'ledger-mode)
(add-to-list 'auto-mode-alist '("\\.ledger$" . ledger-mode))
(add-hook 'ledger-mode-hook
	  (lambda ()
	    (setq-local tab-always-indent 'complete)
	    (setq-local completion-cycle-threshold t)
	    (setq-local ledger-complete-in-steps t)))

(add-to-list 'load-path "/home/gabe/emacs/scss-mode")

;; load el-get
(add-to-list 'load-path "~/.emacs.d/el-get/el-get")

(unless (require 'el-get nil 'noerror)
  (with-current-buffer
      (url-retrieve-synchronously
       "https://raw.githubusercontent.com/dimitri/el-get/master/el-get-install.el")
    (goto-char (point-max))
    (eval-print-last-sexp)))

(add-to-list 'el-get-recipe-path "~/.emacs.d/el-get-user/recipes")
(el-get 'sync)

(setq custom-file "~/.emacs-custom.el")
(load custom-file 'noerror)
(eval-when-compile
  ;; Following line is not needed if use-package.el is in ~/.emacs.d
  ;; (add-to-list 'load-path "<path where use-package is installed>")
  (require 'use-package))

(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
;; Comment/uncomment this line to enable MELPA Stable if desired.  See `package-archive-priorities`
;; and `package-pinned-packages`. Most users will not need or want to do this.
;;(add-to-list 'package-archives '("melpa-stable" . "https://stable.melpa.org/packages/") t)
(package-initialize)


;; (require 'yaml-mode)
;; (add-to-list 'auto-mode-alist '("\\.yml\\'" . yaml-mode))
;; (add-hook 'yaml-mode-hook
;;       '(lambda ()
;; 	 (define-key yaml-mode-map "\C-m" 'newline-and-indent)))

;; (require 'typescript-mode)
;; (add-to-list 'auto-mode-alist '("\\.ts\\'" . typescript-mode))
;; (add-to-list 'auto-mode-alist '("\\.tsx\\'" . typescript-mode))

;; (require 'auto-resize)

;;(set-default-font "-*-fixed-medium-r-*-*-18-*-*-*-*-*-iso8859-*")
(set-face-attribute 'default (selected-frame) :height 100)

(setq-default fill-column 80)
(setq-default py-indent-offset 4)
(setq column-number-mode t)

;; turn off toolbar and menus
(if (fboundp 'tool-bar-mode) (tool-bar-mode -1))
;; (if (fboundp 'menu-bar-mode) (menu-bar-mode -1))

(ansi-color-for-comint-mode-on)

(global-set-key "\C-w" 'backward-kill-word)
(global-set-key "\C-x\C-k" 'kill-region)
(global-set-key "\C-x\C-a" 'beginning-of-line-text)
(global-set-key "\C-x\j" 'setnu-mode)

;; (global-set-key "\M-1" 'other-window)
;; (global-set-key "\M-2" 'other-window)

;; enable cut and paste to and from other programs
(setq select-enable-clipboard t)
; (setq interprogram-paste-function 'x-cut-buffer-or-selection-value)
(global-set-key [(shift delete)] 'clipboard-kill-region)
(global-set-key [(control insert)] 'clipboard-kill-ring-save)
(global-set-key [(shift insert)] 'clipboard-yank)
(global-set-key [f5] 'call-last-kbd-macro)

;; link some more modes to file extensions

(add-to-list 'auto-mode-alist '("\\.asd\\'" . lisp-mode))

;; configuration for React / jsx
(add-to-list 'auto-mode-alist '("\\.jsx?$" . web-mode))
(setq web-mode-content-types-alist '(("jsx" . "\\.js[x]?\\'")))

(defun web-mode-init-hook ()
  "Hooks for Web mode.  Adjust indent."
  (setq web-mode-markup-indent-offset 4))
  
(add-hook 'web-mode-hook  'web-mode-init-hook)

;; flycheck, linting for js
(require 'flycheck)

(setq-default flycheck-disabled-checkers
              (append flycheck-disabled-checkers
                      '(javascript-jshint json-jsonlist)))

;; Enable eslint checker for web-mode
(flycheck-add-mode 'javascript-eslint 'web-mode)
;; Enable flycheck globally
;; (add-hook 'after-init-hook #'global-flycheck-mode)

(defun web-mode-init-prettier-hook ()
  (add-node-modules-path)
  (prettier-js-mode))

(add-hook 'web-mode-hook  'web-mode-init-prettier-hook)

(add-hook 'web-mode-hook  'emmet-mode)

;; javascript mode, set number mode
;; (autoload 'javascript-mode "javascript" nil t)
;; (autoload 'setnu-mode "setnu" nil t)
;; (autoload 'turn-on-setnu-mode "setnu" nil t)
;; (add-hook 'javascript-mode-hook 'turn-on-setnu-mode)

;; markdown mode
(autoload 'markdown-mode "markdown-mode.el"
   "Major mode for editing Markdown files" t)
(add-to-list 'auto-mode-alist '("\\.md\\'" . markdown-mode))
(add-hook 'markdown-mode-hook 'turn-on-auto-fill)


;; octave mode
(autoload 'octave-mode "octave-mode" nil t)
(setq auto-mode-alist
      (cons '("\\.m$" . octave-mode) auto-mode-alist))

;; scss mode
(autoload 'scss-mode "scss-mode.el" "Major mode for editing SCSS" t)
(add-to-list 'auto-mode-alist '("\\.scss\\'" . scss-mode))

;; ord mode
(require 'org)
(define-key global-map "\C-cl" 'org-store-link)
(define-key global-map "\C-ca" 'org-agenda)
(setq org-log-done t)

;; lsp mode
;; (require 'lsp-mode)
;; (add-hook 'prog-mode-hook #'lsp)

;; (use-package lsp-jedi
;;   :ensure t
;;   :config
;;   (with-eval-after-load "lsp-mode"
;;     (add-to-list 'lsp-disabled-clients 'pyls)
;;     (add-to-list 'lsp-enabled-clients 'jedi)))

;; load cycle buffer
(autoload 'cycle-buffer "cycle-buffer" "Cycle forward." t)
(autoload 'cycle-buffer-backward "cycle-buffer" "Cycle backward." t)
(autoload 'cycle-buffer-permissive "cycle-buffer" "Cycle forward allowing *buffers*." t)
(autoload 'cycle-buffer-backward-permissive "cycle-buffer" "Cycle backward allowing *buffers*." t)
(autoload 'cycle-buffer-toggle-interesting "cycle-buffer" "Toggle if this buffer will be considered." t)
(global-set-key [(f8)]        'cycle-buffer-backward)
(global-set-key [(f9)]       'cycle-buffer)
(global-set-key [(shift f8)]  'cycle-buffer-backward-permissive)
(global-set-key [(shift f9)] 'cycle-buffer-permissive)



;; load window number mode
(autoload 'window-number-mode "window-number"
  "A global minor mode that enables selection of windows according to
numbers with the C-x C-j prefix.  Another mode,
`window-number-meta-mode' enables the use of the M- prefix."
  t)


(autoload 'window-number-meta-mode "window-number"
  "A global minor mode that enables use of the M- prefix to select
windows, use `window-number-mode' to display the window numbers in
the mode-line."
  t)

;; (require `window-number)
(window-number-mode 1)
(window-number-meta-mode 1)




;; save all backup files "filename~" to the backup directory
(defvar user-temporary-file-directory
  "~/.emacs_saves")
(make-directory user-temporary-file-directory t)
(setq backup-by-copying t)
(setq backup-directory-alist
      `(("." . ,user-temporary-file-directory)
        (,tramp-file-name-regexp nil)))
(setq auto-save-list-file-prefix
      (concat user-temporary-file-directory ".auto-saves-"))
(setq auto-save-file-name-transforms
      `((".*" ,user-temporary-file-directory t)))

(setq create-lockfiles nil)

;; auto complete
(ac-config-default)
;; (require 'autocomplete)
      
;; (message "My .emacs loaded in %ds" (destructuring-bind (hi lo ms) (current-time)
;;                            (- (+ hi lo) (+ (first *emacs-load-start*) (second *emacs-load-start*)))))

(setq dired-listing-switches "-alh")

;; start working!
(split-window-horizontally)
(dired "/usr/local/src/kotsf-posts/")
(dired "/home/gabe/Dropbox/money/")
(dired "/home/gabe/Dropbox/kotsf/Administration/Accounting")
;; (shell "pyserver")
;; (shell "pyshell")
(balance-windows)
(provide `.emacs)
;;; .emacs ends here
