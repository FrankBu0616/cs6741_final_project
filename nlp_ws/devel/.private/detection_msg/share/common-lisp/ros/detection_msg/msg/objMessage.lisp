; Auto-generated. Do not edit!


(cl:in-package detection_msg-msg)


;//! \htmlinclude objMessage.msg.html

(cl:defclass <objMessage> (roslisp-msg-protocol:ros-message)
  ((obj
    :reader obj
    :initarg :obj
    :type cl:string
    :initform "")
   (score
    :reader score
    :initarg :score
    :type cl:float
    :initform 0.0))
)

(cl:defclass objMessage (<objMessage>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <objMessage>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'objMessage)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name detection_msg-msg:<objMessage> is deprecated: use detection_msg-msg:objMessage instead.")))

(cl:ensure-generic-function 'obj-val :lambda-list '(m))
(cl:defmethod obj-val ((m <objMessage>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader detection_msg-msg:obj-val is deprecated.  Use detection_msg-msg:obj instead.")
  (obj m))

(cl:ensure-generic-function 'score-val :lambda-list '(m))
(cl:defmethod score-val ((m <objMessage>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader detection_msg-msg:score-val is deprecated.  Use detection_msg-msg:score instead.")
  (score m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <objMessage>) ostream)
  "Serializes a message object of type '<objMessage>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'obj))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'obj))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'score))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <objMessage>) istream)
  "Deserializes a message object of type '<objMessage>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'obj) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'obj) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'score) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<objMessage>)))
  "Returns string type for a message object of type '<objMessage>"
  "detection_msg/objMessage")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'objMessage)))
  "Returns string type for a message object of type 'objMessage"
  "detection_msg/objMessage")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<objMessage>)))
  "Returns md5sum for a message object of type '<objMessage>"
  "0ee8aa243ed15ae7496db1e213d462ca")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'objMessage)))
  "Returns md5sum for a message object of type 'objMessage"
  "0ee8aa243ed15ae7496db1e213d462ca")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<objMessage>)))
  "Returns full string definition for message of type '<objMessage>"
  (cl:format cl:nil "string obj~%float64 score~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'objMessage)))
  "Returns full string definition for message of type 'objMessage"
  (cl:format cl:nil "string obj~%float64 score~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <objMessage>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'obj))
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <objMessage>))
  "Converts a ROS message object to a list"
  (cl:list 'objMessage
    (cl:cons ':obj (obj msg))
    (cl:cons ':score (score msg))
))
