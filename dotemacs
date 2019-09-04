;;(require 'cl)
(defvar *emacs-load-start* (current-time))
(setq custom-file "~/.emacs-custom.el")
(load custom-file 'noerror)

(add-to-list 'load-path "/home/gabe/emacs/")
(add-to-list 'load-path "/home/gabe/emacs/yaml-mode")
(add-to-list 'load-path "/home/gabe/emacs/typescript-mode")
(add-to-list 'load-path "/home/gabe/emacs/markdown-mode/")
(add-to-list 'load-path "/home/gabe/slime/")
;; (add-to-list 'load-path "/usr/local/src/ucw-boxset/dep/slime")
;; (add-to-list 'load-path "/usr/local/src/ucw-boxset/dep/slime/contrib")
(add-to-list 'load-path "/home/gabe/emacs/pony-mode")
(add-to-list 'load-path "/home/gabe/emacs/scss-mode")
;; (add-to-list 'load-path "/home/gabe/emacs/auto-resize-emacs")

(require 'package)
(let* ((no-ssl (and (memq system-type '(windows-nt ms-dos))
                    (not (gnutls-available-p))))
       (url (concat (if no-ssl "http" "https") "://melpa.org/packages/")))
  (add-to-list 'package-archives (cons "melpa" url) t))
(when (< emacs-major-version 24)
  ;; For important compatibility libraries like cl-lib
  (add-to-list 'package-archives '("gnu" . "http://elpa.gnu.org/packages/")))
(package-initialize) 

(require 'yaml-mode)
(add-to-list 'auto-mode-alist '("\\.yml\\'" . yaml-mode))
(add-hook 'yaml-mode-hook
      '(lambda ()
	 (define-key yaml-mode-map "\C-m" 'newline-and-indent)))

(require 'typescript-mode)
(add-to-list 'auto-mode-alist '("\\.ts\\'" . typescript-mode))

;; (require 'pony-mode)
;; (require 'auto-resize)

;; (set-default-font "-*-fixed-medium-r-*-*-20-*-*-*-*-*-iso8859-*")
(set-face-attribute 'default (selected-frame) :height 130)

(setq-default fill-column 80)
(setq-default py-indent-offset 4)
(setq column-number-mode t)

;; turn off toolbar and menus
(if (fboundp 'tool-bar-mode) (tool-bar-mode -1))
(if (fboundp 'menu-bar-mode) (menu-bar-mode -1))

(ansi-color-for-comint-mode-on)

(global-set-key "\C-w" 'backward-kill-word)
(global-set-key "\C-x\C-k" 'kill-region)
(global-set-key "\C-x\C-a" 'beginning-of-line-text)
(global-set-key "\C-x\j" 'setnu-mode)

;; enable cut and paste to and from other programs
(setq x-select-enable-clipboard t)
; (setq interprogram-paste-function 'x-cut-buffer-or-selection-value)
(global-set-key [(shift delete)] 'clipboard-kill-region)
(global-set-key [(control insert)] 'clipboard-kill-ring-save)
(global-set-key [(shift insert)] 'clipboard-yank)
(global-set-key [f5] 'call-last-kbd-macro)
;; (global-set-key [f12] 'slime-selector)

;; link some more modes to file extensions

(add-to-list 'auto-mode-alist '("\\.asd\\'" . lisp-mode))

;; javascript mode, set number mode
(autoload 'javascript-mode "javascript" nil t)
(add-to-list 'auto-mode-alist '("\\.js\\'" . rjsx-mode))
(autoload 'setnu-mode "setnu" nil t)
(autoload 'turn-on-setnu-mode "setnu" nil t)
(add-hook 'javascript-mode-hook 'turn-on-setnu-mode)

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

;; configure slime mode
;; (require 'slime)
;; (autoload 'slime-selector "slime" t)
;; (eval-after-load "slime"
;;   '(progn
;;     (setq inferior-lisp-program "sbcl"
;;      lisp-indent-function 'common-lisp-indent-function
;;      common-lisp-hyperspec-root "http://www.lispworks.com/documentation/HyperSpec/")

;;     (slime-setup)
;;     (define-key slime-mode-map "\M-o" 'slime-eval-buffer)
;;     (define-key slime-mode-map "\C-x\q" 'slime-quit-lisp)
;;     (define-key slime-repl-mode-map "\C-x\q" 'slime-quit-lisp)))

;; (add-hook 'slime-load-hook (lambda () (require 'slime-fancy)))
;; (add-hook 'lisp-mode-hook 'turn-on-setnu-mode)
;; (add-hook 'inferior-lisp-mode-hook 'turn-on-setnu-mode)
;; (add-hook 'lisp-mode-hook (lambda () (slime-mode t)))
;; (add-hook 'inferior-lisp-mode-hook (lambda () (inferior-slime-mode t)))

(require 'org)
(define-key global-map "\C-cl" 'org-store-link)
(define-key global-map "\C-ca" 'org-agenda)
(setq org-log-done t)

;; load cycle buffer
(autoload 'cycle-buffer "cycle-buffer" "Cycle forward." t)
(autoload 'cycle-buffer-backward "cycle-buffer" "Cycle backward." t)
(autoload 'cycle-buffer-permissive "cycle-buffer" "Cycle forward allowing *buffers*." t)
(autoload 'cycle-buffer-backward-permissive "cycle-buffer" "Cycle backward allowing *buffers*." t)
(autoload 'cycle-buffer-toggle-interesting "cycle-buffer" "Toggle if this buffer will be considered." t)
(global-set-key [(f9)]        'cycle-buffer-backward)
(global-set-key [(f10)]       'cycle-buffer)
(global-set-key [(shift f9)]  'cycle-buffer-backward-permissive)
(global-set-key [(shift f10)] 'cycle-buffer-permissive)


;; load window number mode
(autoload 'window-number-mode "window-number"
  "A global minor mode that enables selection of windows according to
numbers with the C-x C-j prefix.  Another mode,
`window-number-meta-mode' enables the use of the M- prefix."
  t)

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

(autoload 'window-number-meta-mode "window-number"
  "A global minor mode that enables use of the M- prefix to select
windows, use `window-number-mode' to display the window numbers in
the mode-line."
  t)

(window-number-mode 1)
(window-number-meta-mode 1)

;; save all backup files "filename~" to the backup directory
(defun make-backup-file-name (file)
  (concat "~/.emacs.d/_backups/" (file-name-nondirectory file) "~"))
(put 'downcase-region 'disabled nil)
;; (message "My .emacs loaded in %ds" (destructuring-bind (hi lo ms) (current-time)
;;                            (- (+ hi lo) (+ (first *emacs-load-start*) (second *emacs-load-start*)))))

(setenv "PYTHONPATH" "/home/gabe/python/:.")




;; start working!
(split-window-horizontally)
;; (dired "/usr/local/src/kotsf/")
(dired "/usr/local/src/aeq/")
(dired "/usr/local/src/aeq/aeq/templates/")
(dired "/usr/local/src/aeq/aeq/static/")
;; (dired "/usr/local/src/prophit_dev/prophit_main_repo/")
;; (shell "pyserver")
;; (shell "pyshell")
(balance-windows)

